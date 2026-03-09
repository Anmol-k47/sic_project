"""
WorkMatch Pro v3 — AI Engine
SBERT embeddings + CNN classifier + spaCy skill extraction + RapidFuzz typo correction
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from sentence_transformers import SentenceTransformer, util
import spacy
from spacy.matcher import PhraseMatcher
from rapidfuzz import process as fuzz_proc, fuzz

from config import (SBERT_MODEL, CNN_MAX_WORDS, CNN_MAX_LEN,
                    CNN_EPOCHS, CNN_BATCH_SIZE, CNN_EMBED_DIM, FUZZY_THRESHOLD)
from training_pairs import RAW_PAIRS

tf.get_logger().setLevel("ERROR")


def build_ai_engine(df):
    """Build all AI components: SBERT, CNN, spaCy, fuzzy correction."""

    # ── SBERT embeddings ──
    print("🔍 Encoding with SBERT (all-MiniLM-L6-v2)...")
    sbert = SentenceTransformer(SBERT_MODEL)
    rich = (df["title"].fillna("") + " " +
            df["category"].fillna("") + " " +
            df["skills"].fillna("") + " " +
            df["description"].fillna("")).tolist()
    job_embeds = sbert.encode(rich, convert_to_tensor=True, show_progress_bar=True)
    print(f"✅ SBERT: {len(rich)} embeddings (384D)")

    # ── CNN classifier ──
    print("🧠 Training CNN (400+ pairs, informal-focused)...")
    CATS = sorted(df["category"].dropna().unique().tolist())
    C2I = {c: i for i, c in enumerate(CATS)}
    I2C = {i: c for c, i in C2I.items()}

    PAIRS = [(t, c) for t, c in RAW_PAIRS if c in C2I]
    REPEATS = max(4, 1200 // max(len(PAIRS), 1))
    _xt = [p[0] for p in PAIRS] * REPEATS
    _yl = [C2I[p[1]] for p in PAIRS] * REPEATS

    MW, ML = CNN_MAX_WORDS, CNN_MAX_LEN
    tok = tf.keras.preprocessing.text.Tokenizer(num_words=MW, oov_token="<OOV>")
    tok.fit_on_texts(_xt)
    Xc = tf.keras.preprocessing.sequence.pad_sequences(
        tok.texts_to_sequences(_xt), maxlen=ML, padding="post")
    yc = tf.keras.utils.to_categorical(_yl, num_classes=len(CATS))

    inp = layers.Input(shape=(ML,))
    emb = layers.Embedding(MW, CNN_EMBED_DIM)(inp)
    c1 = layers.Conv1D(128, 3, activation="relu", padding="same")(emb)
    c2 = layers.Conv1D(64, 3, activation="relu", padding="same")(c1)
    gmp = layers.GlobalMaxPooling1D()(c2)
    d1 = layers.Dense(64, activation="relu")(gmp)
    drop = layers.Dropout(0.3)(d1)
    out = layers.Dense(len(CATS), activation="softmax")(drop)

    cnn = Model(inp, out)
    cnn.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    cnn.fit(Xc, yc, epochs=CNN_EPOCHS, batch_size=CNN_BATCH_SIZE, verbose=0)
    print(f"✅ CNN trained: {len(CATS)} categories, {len(PAIRS)} pair types, {len(_xt)} samples")

    def cnn_predict(text):
        pad = tf.keras.preprocessing.sequence.pad_sequences(
            tok.texts_to_sequences([text.lower()]), maxlen=ML, padding="post")
        p = cnn.predict(pad, verbose=0)[0]
        return I2C[int(np.argmax(p))], float(p.max())

    # ── spaCy skill extractor ──
    _nlp = spacy.load("en_core_web_sm")
    _pm = PhraseMatcher(_nlp.vocab, attr="LOWER")
    _kws = [
        "plumbing", "pipe repair", "tap repair", "geyser", "drainage", "sewage",
        "electrician", "wiring", "MCB", "solar panel", "inverter", "lineman",
        "carpentry", "carpenter", "furniture", "modular kitchen", "shuttering",
        "AC repair", "CCTV", "mobile repair", "washing machine repair", "refrigerator repair",
        "painting", "waterproofing", "texture paint", "putty work",
        "mason", "bricklaying", "plastering", "tile fixing", "bar bending", "welding", "excavation",
        "driving", "delivery", "logistics", "cab driver", "truck driver", "auto rickshaw",
        "cooking", "cleaning", "mopping", "childcare", "elder care", "babysitter", "home cook",
        "farming", "crop harvesting", "tractor driving", "dairy", "vegetable vendor", "fish selling", "irrigation",
        "tailoring", "stitching", "sewing", "embroidery", "weaving", "dry cleaning", "garment",
        "security guard", "housekeeping", "watchman", "office boy", "parking",
        "CNC operator", "quality checking", "packing", "ITI fitter", "forklift",
        "beautician", "barber", "mehndi", "haircut", "waxing", "salon",
        "nursing", "patient care", "ANM", "lab technician", "vaccination",
        "telecalling", "data entry", "customer care", "call center",
        "field sales", "insurance", "retail sales", "FMCG",
        "street food", "hawker", "scrap collection", "sanitation", "kabaadi",
    ]
    _pm.add("SK", [_nlp.make_doc(k) for k in _kws])

    def extract_skills(text):
        doc = _nlp(text.lower())
        return list(set(doc[s:e].text for _, s, e in _pm(doc)))

    # ── City detection ──
    city_map = {c.lower(): c for c in df["location"].dropna().unique() if len(c) > 1}

    def detect_city(q):
        ql = q.lower()
        for k, v in city_map.items():
            if k in ql:
                return v
        return None

    # ── Query expansion + RapidFuzz ──
    SYN = {
        "driver": "driver car vehicle LMV transport",
        "delivery": "delivery rider bike courier last mile",
        "cook": "cooking food kitchen chef meals",
        "clean": "cleaning mopping sweeping domestic",
        "farm": "farming agriculture crop field",
        "tailor": "tailor stitching sewing",
        "guard": "security guard watchman patrol",
        "mobile": "mobile phone repair technician",
        "ac": "air conditioner cooling HVAC repair",
    }
    FUZZY_VOCAB = [
        "electrician", "plumber", "carpenter", "welder", "painter", "mason", "driver",
        "delivery", "mechanic", "technician", "tailor", "barber", "beautician", "cook",
        "nurse", "guard", "security", "helper", "labourer", "farmer", "vendor",
        "hawker", "ragpicker", "sanitation", "dhobi", "cobbler", "housekeeping",
    ]

    def fuzzy_correct(word, threshold=FUZZY_THRESHOLD):
        if len(word) < 4:
            return word
        match, score, _ = fuzz_proc.extractOne(word, FUZZY_VOCAB, scorer=fuzz.ratio)
        return match if score >= threshold else word

    def expand_query(q):
        words = q.lower().split()
        corrected = [fuzzy_correct(w) for w in words]
        out = list(corrected)
        for w in corrected:
            if w in SYN:
                out.extend(SYN[w].split())
        return " ".join(out)

    return sbert, job_embeds, cnn_predict, extract_skills, detect_city, expand_query, CATS
