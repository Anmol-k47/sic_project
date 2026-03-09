"""
WorkMatch Pro v4 — SQLite Database Module (Live Data Edition)
"""

import sqlite3
import pandas as pd
from config import DB_PATH


def init_db():
    """Create database and jobs table with v4 schema."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, category TEXT, location TEXT,
        salary TEXT DEFAULT 'Not disclosed',
        experience TEXT DEFAULT 'Not specified',
        company TEXT DEFAULT '', skills TEXT DEFAULT '',
        description TEXT DEFAULT '', source TEXT DEFAULT '',
        vehicle_owned TEXT DEFAULT '', migrant TEXT DEFAULT '',
        nco_code TEXT DEFAULT '', nco_sector TEXT DEFAULT '',
        work_type TEXT DEFAULT 'Full-time',
        min_education TEXT DEFAULT 'No requirement',
        salary_type TEXT DEFAULT 'monthly',
        salary_min_mo INTEGER DEFAULT 0,
        live_url TEXT DEFAULT '',
        posted_date TEXT DEFAULT ''
    )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_cat ON jobs(category)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_loc ON jobs(location)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_src ON jobs(source)")
    conn.commit()
    return conn


def bulk_insert(conn, df):
    """Insert rows from DataFrame, skipping duplicates."""
    c = conn.cursor()
    n = 0
    for _, r in df.iterrows():
        t = str(r.get("title", "")).strip()
        loc = str(r.get("location", "")).strip()
        src = str(r.get("source", ""))
        if len(t) < 2:
            continue
        c.execute("SELECT 1 FROM jobs WHERE title=? AND location=? AND source=?", (t, loc, src))
        if c.fetchone():
            continue
        c.execute("""INSERT INTO jobs
            (title,category,location,salary,experience,company,skills,description,source,
             vehicle_owned,migrant,nco_code,nco_sector,work_type,min_education,salary_type,
             salary_min_mo,live_url,posted_date)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            t, str(r.get("category", "")).strip(), loc,
            str(r.get("salary", "Not disclosed")),
            str(r.get("experience", "Not specified")),
            str(r.get("company", "")),
            str(r.get("skills", "")),
            str(r.get("description", "")),
            src,
            str(r.get("vehicle_owned", "")),
            str(r.get("migrant", "")),
            str(r.get("nco_code", "")),
            str(r.get("nco_sector", "")),
            str(r.get("work_type", "Full-time")),
            str(r.get("min_education", "No requirement")),
            str(r.get("salary_type", "monthly")),
            int(r.get("salary_min_mo", 0)),
            str(r.get("live_url", "")),
            str(r.get("posted_date", "")),
        ))
        n += 1
    conn.commit()
    return n


def build_database(seed_df):
    """Build the database with seed + live data, return DataFrame + stats."""
    from live_data import (build_live_jobs_batch, fetch_eshram_dashboard_stats,
                           fetch_plfs_wage_data, enrich_jobs_with_live_salary)

    print("\n" + "═" * 62)
    print("  🗄️  WorkMatch v4 — Informal Sector Database (Live+Seed)")
    print("═" * 62)
    conn = init_db()
    c = conn.cursor()

    # Load seed data
    c.execute("SELECT COUNT(*) FROM jobs WHERE source LIKE 'seed%'")
    existing_seed = c.fetchone()[0]
    if existing_seed < 10:
        n = bulk_insert(conn, seed_df)
        print(f"   ✦ Inserted {n} NCO-verified seed jobs")
    else:
        print(f"   ✦ Seed data: {existing_seed} rows (already loaded)")

    # Fetch live Adzuna jobs
    live_df = build_live_jobs_batch()
    if not isinstance(live_df, list) and not live_df.empty:
        n_live = bulk_insert(conn, live_df)
        print(f"   🌐 Inserted {n_live} live Adzuna jobs")
    else:
        print("   ℹ️  Adzuna live jobs: not loaded (no API keys or no network)")
        print("      → Set ADZUNA_APP_ID + ADZUNA_APP_KEY in .env for live job feeds")

    # Fetch live eShram stats
    print("\n📡 Fetching live eShram/OGD sector statistics...")
    eshram_stats = fetch_eshram_dashboard_stats()
    plfs_data = fetch_plfs_wage_data()

    df = pd.read_sql("SELECT * FROM jobs", conn)
    df = enrich_jobs_with_live_salary(df, plfs_data)

    c.execute("SELECT category, COUNT(*), MAX(source) FROM jobs GROUP BY category ORDER BY COUNT(*) DESC")
    cat_stats = {row[0]: {"count": row[1], "has_live": "adzuna" in str(row[2])} for row in c.fetchall()}
    conn.close()

    live_count = len(df[df["source"] == "adzuna_live"])
    seed_count = len(df) - live_count
    print(f"\n📊 Database: {len(df)} jobs | {len(df['category'].unique())} categories | "
          f"{len(df['location'].unique())} cities")
    print(f"   🌐 Live (Adzuna): {live_count} | 📚 Verified Seed (eShram NCO): {seed_count}")

    print(f"\n📡 eShram Live Stats ({len(eshram_stats)} sectors):")
    for sector, count in list(eshram_stats.items())[:5]:
        c_str = f"{int(count):,}" if isinstance(count, (int, float)) else str(count)
        print(f"   • {sector}: {c_str} workers")

    return df, cat_stats, eshram_stats
