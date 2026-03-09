"""
WorkMatch Pro v4 — Matching Pipeline
SBERT + CNN hybrid matching with 7 filters + live data integration.
"""

import re
import sqlite3
import numpy as np
import pandas as pd
from sentence_transformers import util

from config import (SBERT_WEIGHT, CAT_BONUS_WEIGHT, LIVE_BONUS_WEIGHT,
                    CNN_CONFIDENCE_THRESHOLD, MIN_MATCH_SCORE,
                    ADZUNA_APP_ID, ADZUNA_APP_KEY, DB_PATH)
from salary_benchmarks import ESHRAM_SECTOR_MAP


RESULT_COLS = ["Job Title", "Category", "Location", "Salary", "Experience",
               "Work Type", "Match %", "Source", "NCO", "Live Link"]
EMPTY_DF = pd.DataFrame(columns=RESULT_COLS)


def _badge(p):
    if p >= 75: return f"🟢 {p:.0f}%"
    if p >= 45: return f"🟡 {p:.0f}%"
    return f"🔴 {p:.0f}%"


def _source_badge(src):
    if "adzuna" in str(src): return "🌐 Live"
    return "📚 NCO"


def _exp_overlap(ui_filter, job_exp):
    if ui_filter == "Any Experience":
        return True
    u = [int(x) for x in re.findall(r'\d+', ui_filter)]
    j = [int(x) for x in re.findall(r'\d+', job_exp)]
    if not u or not j:
        return True
    u_min, u_max = u[0], u[1] if len(u) > 1 else u[0] + 2
    j_min, j_max = j[0], j[1] if len(j) > 1 else j[0] + 2
    return not (u_max < j_min or j_max < u_min)


def _active_filters_html(cat, city, exp_f, vehicle, migrant, work_type, cnn_cat, cnn_conf):
    parts = []
    if cat != "All":
        parts.append(f"📂 <b>Category:</b> {cat}")
    elif cnn_conf > CNN_CONFIDENCE_THRESHOLD:
        parts.append(f"🤖 <b>AI detected:</b> {cnn_cat} ({cnn_conf:.0%})")
    if city != "All":           parts.append(f"📍 <b>City:</b> {city}")
    if exp_f != "Any Experience": parts.append(f"🎓 <b>Exp:</b> {exp_f}")
    if vehicle != "Any":        parts.append(f"🚗 <b>Vehicle:</b> {vehicle}")
    if migrant != "Any":        parts.append(f"🏠 <b>Worker:</b> {migrant}")
    if work_type != "Any":      parts.append(f"💼 <b>Type:</b> {work_type}")
    if not parts:               parts.append("🔍 <b>All jobs</b> — no filters applied")
    return "<div class='info'>" + " &nbsp;|&nbsp; ".join(parts) + "</div>"


def make_pipeline(df, sbert, job_embeds, cnn_predict, extract_skills,
                  detect_city, expand_query, eshram_stats):
    """Create the search pipeline function with live data support."""

    def pipeline(query, city, cat, exp_filter, top_k,
                 vehicle_filter="Any", migrant_filter="Any", work_type_filter="Any"):

        if not query or not str(query).strip():
            return EMPTY_DF, "<div class='info'>⬅️ Enter a job description and click Search</div>", "", ""

        query = str(query).strip()
        cc, conf = cnn_predict(query)

        # Live refresh: pull fresh Adzuna jobs for this query
        if ADZUNA_APP_ID and ADZUNA_APP_KEY:
            from live_data import fetch_adzuna_jobs
            from database import bulk_insert
            fresh = fetch_adzuna_jobs(query, results=5)
            if fresh:
                fdf = pd.DataFrame(fresh)
                conn = sqlite3.connect(DB_PATH)
                bulk_insert(conn, fdf)
                conn.close()

        # Active category
        if cat != "All":          active_cat = cat.strip()
        elif conf > CNN_CONFIDENCE_THRESHOLD: active_cat = cc
        else:                     active_cat = "All"

        # Active city
        if city != "All":         active_city = city.strip()
        else:
            dc = detect_city(query)
            active_city = dc if dc else "All"

        skills = extract_skills(query)
        expanded = expand_query(query)

        # SBERT scoring
        q_emb = sbert.encode(expanded, convert_to_tensor=True)
        scores = util.cos_sim(q_emb, job_embeds)[0].cpu().numpy()
        cat_bonus = np.where(df["category"].str.strip().values == active_cat, CAT_BONUS_WEIGHT, 0.0)
        live_bonus = np.where(df["source"].str.contains("adzuna", na=False).values, LIVE_BONUS_WEIGHT, 0.0)
        raw_scores = SBERT_WEIGHT * scores + (1 - SBERT_WEIGHT - LIVE_BONUS_WEIGHT) * cat_bonus + live_bonus

        if raw_scores.max() < MIN_MATCH_SCORE:
            msg = ("<div class='info' style='border-left-color:#f59e0b'>"
                   "🤔 <b>No confident match.</b> Try more specific terms.</div>")
            return EMPTY_DF, msg, "", ""

        mx = raw_scores.max()
        pcts = raw_scores / mx * 100

        res = df.copy()
        res["_score"] = pcts
        res["_raw"] = raw_scores
        res = res[res["_raw"] >= MIN_MATCH_SCORE].copy()

        # Apply filters
        if active_cat != "All":
            res = res[res["category"].str.strip() == active_cat]
        if active_city != "All":
            res = res[res["location"].str.strip().str.lower() == active_city.strip().lower()]
        if exp_filter != "Any Experience":
            res = res[res["experience"].apply(lambda e: _exp_overlap(exp_filter, str(e)))]
        if vehicle_filter == "Two-Wheeler":
            res = res[res["vehicle_owned"].str.strip() == "two-wheeler"]
        elif vehicle_filter == "Four-Wheeler":
            res = res[res["vehicle_owned"].str.strip() == "four-wheeler"]
        elif vehicle_filter == "No Vehicle Required":
            res = res[res["vehicle_owned"].str.strip() == "no"]
        if migrant_filter == "Open to migrants":
            res = res[res["migrant"].str.strip() == "yes"]
        elif migrant_filter == "Local only":
            res = res[res["migrant"].str.strip() == "no"]
        if work_type_filter != "Any":
            res = res[res["work_type"].str.strip() == work_type_filter]

        res = res.drop_duplicates(subset=["title", "location"])
        res = res.sort_values("_score", ascending=False).head(int(top_k))

        if res.empty:
            active = []
            if active_cat != "All":            active.append(f"Category='{active_cat}'")
            if active_city != "All":           active.append(f"City='{active_city}'")
            if exp_filter != "Any Experience":  active.append(f"Exp='{exp_filter}'")
            msg = (f"<div class='info'>⚠️ No jobs found with: "
                   f"<b>{', '.join(active) if active else 'no filters'}</b>. "
                   f"Try removing filters.</div>")
            return EMPTY_DF, msg, "", ""

        # Format output
        res["Match %"] = res["_score"].apply(_badge)
        res["Source"] = res["source"].apply(_source_badge)
        if "live_url" not in res.columns:
            res["live_url"] = ""
        res["Live Link"] = res["live_url"].apply(
            lambda u: f"<a href='{u}' target='_blank'>Apply →</a>" if u else "")

        out = res[["title", "category", "location", "salary", "experience",
                    "work_type", "Match %", "Source", "nco_code", "live_url"]].copy()
        out.columns = RESULT_COLS

        filter_html = _active_filters_html(
            active_cat, active_city, exp_filter,
            vehicle_filter, migrant_filter, work_type_filter, cc, conf)

        sk_str = " · ".join(skills) if skills else "None detected"
        exp_str = (expanded[:100] + "...") if len(expanded) > 100 else expanded

        # eShram live worker count
        eshram_html = ""
        for sector, cats in ESHRAM_SECTOR_MAP.items():
            if active_cat in cats and sector in eshram_stats:
                count = eshram_stats[sector]
                c_str = f"{int(count):,}" if isinstance(count, (int, float)) else str(count)
                eshram_html = (f" &nbsp;|&nbsp; 📊 <b>eShram Live:</b> "
                               f"<b>{c_str}</b> workers in '{sector}'")
                break

        skill_html = f"<div class='info'>🛠️ <b>Skills detected:</b> {sk_str}{eshram_html}</div>"
        expand_html = f"<div class='info'>🔡 <b>Query expanded:</b> <i>{exp_str}</i></div>"

        return out, filter_html, skill_html, expand_html

    return pipeline
