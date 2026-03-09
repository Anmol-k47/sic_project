"""
WorkMatch Pro v4 — Gradio UI (Live Data Edition)
"""

import pandas as pd
import gradio as gr
from styles import CSS
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY
from salary_benchmarks import OFFICIAL_SALARY_BENCHMARKS


def build_ui(df, pipeline_fn, db_stats, eshram_stats):
    """Build the Gradio web interface with live data indicators."""
    CITIES = ["All"] + sorted(df["location"].dropna().unique().tolist())
    CATS_UI = ["All"] + sorted(df["category"].dropna().unique().tolist())
    EXP = ["Any Experience",
           "0-1 yrs", "0-2 yrs", "0-3 yrs", "1-3 yrs", "1-4 yrs",
           "2-4 yrs", "2-5 yrs", "3-5 yrs", "3-6 yrs", "3-7 yrs", "5-8 yrs"]
    WORK_TYPES = ["Any", "Full-time", "Part-time", "Gig-Daily"]

    total = len(df)
    cn = len(CATS_UI) - 1
    ctn = len(CITIES) - 1
    has_live = bool(ADZUNA_APP_ID and ADZUNA_APP_KEY)
    live_cnt = len(df[df["source"].str.contains("adzuna", na=False)])
    total_workers = sum(v for v in eshram_stats.values() if isinstance(v, (int, float)))

    live_pill = ("<span class='pill g'>🌐 Adzuna Live</span>" if has_live
                 else "<span class='pill'>📚 Seed Mode (add API keys)</span>")
    live_status = (
        "<div style='margin-top:.7rem;font-size:.7rem;color:#4ade80'>"
        "✅ LIVE DATA ACTIVE — Adzuna India API connected</div>" if has_live else
        "<div style='margin-top:.7rem;font-size:.7rem;color:#f59e0b'>"
        "ℹ️ Add ADZUNA_APP_ID + ADZUNA_APP_KEY to .env for live job feeds</div>")

    HEADER = f"""
<div class="hero">
  <div class="logo">⚡ WorkMatch Pro</div>
  <div class="tag">India Informal Sector · AI-Powered · Live + NCO-Verified Data</div>
  <div class="pills">
    <span class="pill o">🌾 Agriculture</span><span class="pill o">🔧 Construction</span>
    <span class="pill o">🚗 Transport & Gig</span><span class="pill o">🏠 Domestic</span>
    <span class="pill o">🧵 Apparel</span><span class="pill o">🌿 Street Vending</span>
    {live_pill}
    <span class="pill">eShram NCO</span><span class="pill">MoSPI PLFS</span>
    <span class="pill">NITI Aayog</span><span class="pill">ILO India</span>
  </div>
  <div class="stats">
    <div class="st"><div class="sn">{total}</div><div class="sl">Jobs</div></div>
    <div class="st"><div class="sn">{live_cnt}</div><div class="sl">🌐 Live</div></div>
    <div class="st"><div class="sn">{cn}</div><div class="sl">Categories</div></div>
    <div class="st"><div class="sn">{ctn}</div><div class="sl">Cities</div></div>
    <div class="st"><div class="sn">{int(total_workers/1e6):.0f}M</div><div class="sl">eShram Workers</div></div>
    <div class="st"><div class="sn">NCO</div><div class="sl">Anchored</div></div>
  </div>
  {live_status}
</div>"""

    EX = [
        ["plumber pipe repair water tap leak bathroom",       "All","All","Any Experience",6,"Any","Any","Any"],
        ["electrician wiring switch MCB fan repair",          "All","All","Any Experience",6,"Any","Any","Any"],
        ["maid cleaning sweeping mopping cooking domestic",   "All","All","Any Experience",6,"Any","Any","Any"],
        ["farm worker crop harvest field daily wage",         "All","All","Any Experience",6,"Any","Any","Any"],
        ["delivery rider bike Swiggy Zomato food GPS",        "All","All","Any Experience",6,"Any","Any","Gig-Daily"],
        ["mason bricklaying cement wall plaster construction","All","All","Any Experience",6,"Any","Any","Any"],
        ["tailor stitching sewing blouse kurta alteration",   "All","All","Any Experience",6,"Any","Any","Any"],
        ["vegetable vendor fruit cart market selling",        "All","All","Any Experience",6,"Any","Any","Any"],
        ["security guard watchman patrol night shift",        "All","All","Any Experience",6,"Any","Any","Any"],
        ["AC technician air conditioner repair gas filling",  "All","All","Any Experience",6,"Any","Any","Any"],
        ["barber haircut shave salon naai trim beard",        "All","All","Any Experience",6,"Any","Any","Any"],
        ["waste picker scrap kabaadi recycling collection",   "All","All","Any Experience",6,"Any","Any","Any"],
    ]

    # Live data status bar
    live_sources = []
    if eshram_stats:
        live_sources.append(f"eShram: {len(eshram_stats)} sectors")
    if has_live:
        live_sources.append("Adzuna India: live job feed active")
    live_bar = " &nbsp;·&nbsp; ".join(live_sources) or "Running in offline seed mode"

    with gr.Blocks(theme=gr.themes.Base(), css=CSS, title="WorkMatch Pro v4") as demo:
        gr.HTML(HEADER)
        gr.HTML(f"<div class='info' style='text-align:center;margin:.3rem 0'>📡 <b>Live data:</b> "
                f"{live_bar} &nbsp;·&nbsp; 🕐 Cache: 6h TTL &nbsp;·&nbsp; "
                f"Salaries: MoSPI PLFS 2022-23 + NITI Aayog 2023</div>")

        with gr.Row():
            with gr.Column(scale=1, min_width=300, elem_classes=["panel"]):
                gr.Markdown("### 🔍 Search Jobs")
                gr.Markdown("*Describe the job or worker skills (Hindi/English)*")
                query = gr.Textbox(label="Job Query",
                    placeholder='"plumber pipe repair"  or  "delivery rider bike"  or  "mason cement wall"',
                    lines=3)
                with gr.Row():
                    city = gr.Dropdown(CITIES, value="All", label="📍 City")
                    cat = gr.Dropdown(CATS_UI, value="All", label="📂 Category")
                with gr.Row():
                    exp_f = gr.Dropdown(EXP, value="Any Experience", label="🎓 Experience")
                    work_type_f = gr.Dropdown(WORK_TYPES, value="Any", label="💼 Work Type")
                vehicle = gr.Dropdown(
                    ["Any", "Two-Wheeler", "Four-Wheeler", "No Vehicle Required"],
                    value="Any", label="🚗 Vehicle Owned")
                migrant = gr.Dropdown(
                    ["Any", "Open to migrants", "Local only"],
                    value="Any", label="🏠 Worker Type")
                top_k = gr.Slider(1, 15, value=6, step=1, label="Results Count")
                btn = gr.Button("🔍 Search Jobs →", elem_classes=["sbtn"])
                gr.Markdown("### 💡 Quick Examples")
                gr.Examples(examples=EX,
                            inputs=[query, city, cat, exp_f, top_k, vehicle, migrant, work_type_f],
                            label="")

            with gr.Column(scale=2, elem_classes=["panel"]):
                gr.Markdown("### 📊 Matching Jobs")
                gr.HTML("<div class='info' style='font-size:.7rem'>🌐 = Live Adzuna job "
                        "&nbsp;|&nbsp; 📚 = NCO-verified seed &nbsp;|&nbsp; "
                        "Salaries from MoSPI/NITI Aayog/ILO official sources</div>")
                filter_md = gr.HTML("<div class='info'>⬅️ Enter a job description and click "
                                   "<b>Search Jobs →</b></div>")
                skill_md = gr.HTML("<div class='info'>&nbsp;</div>")
                sys_md = gr.HTML("<div class='info'>&nbsp;</div>")
                result_df = gr.Dataframe(interactive=False, wrap=True)

        btn.click(fn=pipeline_fn,
                  inputs=[query, city, cat, exp_f, top_k, vehicle, migrant, work_type_f],
                  outputs=[result_df, filter_md, skill_md, sys_md])

        # Salary benchmarks section
        gr.Markdown("---")
        gr.Markdown("### 💰 Official Salary Benchmarks (MoSPI PLFS / NITI Aayog / ILO)")
        bench_data = []
        for cat_name, b in OFFICIAL_SALARY_BENCHMARKS.items():
            if "daily_min" in b:
                sal = f"₹{b['daily_min']}-{b['daily_max']}/day"
            else:
                sal = f"₹{b['mo_min']:,}-{b['mo_max']:,}/mo"
            bench_data.append([cat_name, sal, b["source"]])
        bench_df = pd.DataFrame(bench_data, columns=["Category", "Salary Range", "Official Source"])
        gr.Dataframe(bench_df, interactive=False)

        gr.HTML("""
        <div class='info' style='margin-top:.5rem;font-size:.72rem'>
          <b>Data Sources:</b>
          MoSPI PLFS 2022-23 Annual Report (Table 23, Average Wages) ·
          NITI Aayog India's Booming Gig and Platform Economy 2023 ·
          ILO India Wages in the Informal Economy 2023 ·
          eShram/NDUW Portal (eshram.gov.in) ·
          PSARA Minimum Wages for Security Guards 2023 ·
          NASSCOM IT-BPM Workforce Report 2023 ·
          NCS Portal (ncs.gov.in) ·
          NSSO Agricultural Wages Survey 2022-23
        </div>""")

    return demo
