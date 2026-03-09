"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         WorkMatch Pro v4 — INDIA INFORMAL SECTOR (LIVE DATA)               ║
║                                                                             ║
║  LIVE DATA SOURCES (fetched at startup & cached for 6h):                   ║
║   1. Adzuna India API  → real job vacancies                                ║
║   2. OGD data.gov.in   → eShram sector/worker stats                       ║
║   3. NCS Portal        → government job fair & vacancy counts              ║
║   4. MoSPI PLFS        → official salary benchmarks                        ║
║   5. eSHRAM Dashboard  → live worker registration counts                   ║
║                                                                             ║
║  HOW TO USE:                                                                ║
║   Set API keys in .env file, then: python app.py                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")


def _install():
    """Auto-install all dependencies."""
    print("⚙️  Installing dependencies (~2 min first time)...")
    pkgs = [
        "gradio==4.44.0", "pandas", "numpy", "tensorflow", "spacy",
        "sentence-transformers", "rapidfuzz", "matplotlib", "scikit-learn",
        "Pillow", "requests", "cachetools",
    ]
    for p in pkgs:
        try:
            __import__(p.split("==")[0].replace("-", "_"))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", p])
    try:
        import spacy
        spacy.load("en_core_web_sm")
    except OSError:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    print("✅ All dependencies ready.\n")


if __name__ == "__main__":
    from config import ADZUNA_APP_ID, DATA_GOV_KEY

    print("\n⚡ WorkMatch Pro v4 — India Informal Sector (LIVE DATA)")
    print("=" * 62)
    print(f"  Adzuna API: {'✅ Connected' if ADZUNA_APP_ID else '⚠️  Not set (add to .env)'}")
    print(f"  OGD API:    {'✅ Connected' if DATA_GOV_KEY else 'ℹ️  Using public endpoint'}")
    print("=" * 62)

    print("\n[0/5] ⚙️  Checking dependencies...")
    _install()

    from data_loader import load_seed_data
    from database import build_database
    from ai_engine import build_ai_engine
    from pipeline import make_pipeline
    from verification import run_verification
    from ui import build_ui

    print("[1/5] 🗄️  Building database (seed + live)...")
    seed_df = load_seed_data()
    df, db_stats, eshram_stats = build_database(seed_df)

    print(f"\n[2/5] 🧠  Training AI engine ({len(df)} jobs)...")
    sbert, job_embeds, cnn_predict, extract_skills, detect_city, expand_query, CATS = \
        build_ai_engine(df)

    print("\n[3/5] 🔗  Assembling pipeline...")
    pipeline_fn = make_pipeline(
        df, sbert, job_embeds, cnn_predict, extract_skills,
        detect_city, expand_query, eshram_stats)

    print("\n[4/5] 🧪  Running verification tests...")
    score = run_verification(pipeline_fn)
    if score < 60:
        print(f"⚠️  Score {score:.0f}% — check CNN pairs or seed data")
    else:
        print(f"✅ Verification passed ({score:.0f}%)")

    print("\n[5/5] 🚀  Launching Gradio UI...")
    demo = build_ui(df, pipeline_fn, db_stats, eshram_stats)

    print("\n✅ WorkMatch Pro v4 ready!")
    if not ADZUNA_APP_ID:
        print("\n  To enable LIVE job feeds:")
        print("  1. Register free at https://developer.adzuna.com/")
        print("  2. Create .env file:")
        print("     ADZUNA_APP_ID=your_id")
        print("     ADZUNA_APP_KEY=your_key")
        print("  3. Restart — Adzuna will auto-fetch 200+ live India jobs\n")
        print("  To enable OGD eShram live stats:")
        print("  1. Register at https://data.gov.in/user/register")
        print("  2. Add to .env: DATA_GOV_API_KEY=your_key\n")

    demo.launch(share=True, inline=False)
