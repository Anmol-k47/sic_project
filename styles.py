"""
WorkMatch Pro v4 — UI Styles (CSS) — Live Data Edition
"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500&display=swap');
:root{--bg:#07080f;--surface:#0d1117;--card:#111827;--border:#1e2d3d;
  --blue:#3b82f6;--green:#22c55e;--orange:#f97316;--text:#f1f5f9;--muted:#64748b;--r:10px;}
body,.gradio-container{background:var(--bg)!important;font-family:'Inter',sans-serif!important;color:var(--text)!important;}
.hero{background:linear-gradient(135deg,#0d1117 0%,#091428 50%,#0d1117 100%);border-bottom:1px solid var(--border);padding:2rem 1rem 1.5rem;text-align:center;}
.logo{font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#f97316,#3b82f6,#22c55e);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1.5px;}
.tag{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;margin-top:.3rem;}
.pills{display:flex;flex-wrap:wrap;gap:.4rem;justify-content:center;margin-top:.9rem;}
.pill{background:#1a2a3a;color:#60a5fa;border:1px solid #2d4a6b;border-radius:100px;padding:.2rem .75rem;font-size:.66rem;font-family:'IBM Plex Mono',monospace;}
.pill.o{color:#fb923c;border-color:#7c2d12;background:#1c0d05;}
.pill.g{color:#4ade80;border-color:#14532d;background:#052005;}
.stats{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;margin-top:1rem;}
.st{background:rgba(30,45,61,.6);border:1px solid var(--border);border-radius:8px;padding:.45rem .9rem;text-align:center;min-width:80px;}
.sn{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--orange);}
.sl{font-size:.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;}
.panel{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important;}
label span{color:var(--text)!important;font-size:.72rem!important;font-weight:600!important;letter-spacing:.05em!important;text-transform:uppercase!important;font-family:'IBM Plex Mono',monospace!important;}
textarea,input{background:#090e18!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
textarea:focus,input:focus{border-color:var(--orange)!important;box-shadow:0 0 0 2px rgba(249,115,22,.15)!important;}
select{background:#090e18!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
.sbtn{background:linear-gradient(135deg,#c2410c,#ea580c)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-family:'IBM Plex Mono',monospace!important;font-size:.78rem!important;font-weight:600!important;width:100%!important;cursor:pointer!important;transition:all .2s!important;}
.sbtn:hover{background:linear-gradient(135deg,#ea580c,#f97316)!important;transform:translateY(-1px);box-shadow:0 4px 14px rgba(249,115,22,.3)!important;}
.info{background:#090e18;border:1px solid var(--border);border-left:3px solid var(--orange);border-radius:8px;padding:.6rem 1rem;font-size:.82rem;margin:.2rem 0;}
.lbadge{background:#052e16;color:#4ade80;border:1px solid #14532d;border-radius:4px;padding:.1rem .4rem;font-size:.65rem;font-family:'IBM Plex Mono',monospace;}
.gr-dataframe table{background:var(--card)!important;border-collapse:collapse!important;width:100%!important;}
.gr-dataframe th{background:#090e18!important;color:var(--orange)!important;font-family:'IBM Plex Mono',monospace!important;font-size:.62rem!important;text-transform:uppercase!important;letter-spacing:.1em!important;padding:.7rem 1rem!important;border-bottom:2px solid var(--border)!important;}
.gr-dataframe td{color:var(--text)!important;padding:.55rem 1rem!important;border-bottom:1px solid var(--border)!important;font-size:.82rem!important;}
.gr-dataframe tr:hover td{background:rgba(249,115,22,.04)!important;}
::-webkit-scrollbar{width:5px;background:var(--bg);}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
"""

CATEGORY_COLORS = {
    "Plumbing": "#0ea5e9", "Electrical Work": "#fbbf24", "Carpentry": "#a16207",
    "AC & Appliance Repair": "#06b6d4", "Painting": "#d946ef", "Masonry": "#78716c",
    "Gig Delivery": "#84cc16", "Driver": "#22c55e",
    "Domestic (Cleaning)": "#ec4899", "Domestic (Cook/Care)": "#f472b6",
    "Food & Hospitality": "#a78bfa",
    "Agriculture (Crops)": "#65a30d", "Agriculture (Livestock)": "#4ade80",
    "Agriculture (Vendor)": "#86efac", "Apparel & Textile": "#e879f9",
    "Security & Facility": "#94a3b8", "Manufacturing": "#f97316",
    "Beauty & Wellness": "#fb7185", "Healthcare (Para)": "#ef4444",
    "BPO & Telecalling": "#6366f1", "Field Sales & Retail": "#f43f5e",
    "Street Vending": "#fb923c", "Waste & Recycling": "#6b7280",
}
