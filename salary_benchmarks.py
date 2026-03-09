"""
WorkMatch Pro v4 — Official Salary Benchmarks & Sector Mappings
Sources: MoSPI PLFS 2022-23, NITI Aayog Gig Economy 2023, ILO India 2023
"""

# ── eShram sector → our categories ──────────────────────────────
ESHRAM_SECTOR_MAP = {
    "Agriculture": ["Agriculture (Crops)", "Agriculture (Livestock)", "Agriculture (Vendor)"],
    "Construction": ["Masonry", "Plumbing", "Electrical Work", "Carpentry", "Painting"],
    "Domestic and Household Workers": ["Domestic (Cleaning)", "Domestic (Cook/Care)"],
    "Transport": ["Driver", "Gig Delivery"],
    "Apparel and Textile": ["Apparel & Textile"],
    "Food Processing": ["Food & Hospitality"],
    "Trade and Commerce": ["Field Sales & Retail", "Street Vending"],
    "Health and Personal Care": ["Beauty & Wellness", "Healthcare (Para)"],
    "Other Services": ["BPO & Telecalling", "Security & Facility", "Manufacturing", "Waste & Recycling"],
}

# ── NCO Code → category (official ILO/eShram) ───────────────────
NCO_CATEGORY_MAP = {
    "7126": "Plumbing", "7411": "Electrical Work", "7115": "Carpentry",
    "7233": "AC & Appliance Repair", "7131": "Painting",
    "7112": "Masonry", "9313": "Masonry",
    "8321": "Gig Delivery", "8322": "Driver", "8332": "Driver",
    "9111": "Domestic (Cleaning)", "9112": "Domestic (Cook/Care)",
    "5120": "Food & Hospitality", "5131": "Food & Hospitality",
    "9211": "Agriculture (Crops)", "8341": "Agriculture (Crops)",
    "6121": "Agriculture (Livestock)", "6122": "Agriculture (Livestock)",
    "9214": "Agriculture (Vendor)",
    "7531": "Apparel & Textile", "7533": "Apparel & Textile", "8153": "Apparel & Textile",
    "5414": "Security & Facility",
    "7223": "Manufacturing", "9321": "Manufacturing", "7543": "Manufacturing",
    "5142": "Beauty & Wellness", "5141": "Beauty & Wellness",
    "3221": "Healthcare (Para)", "2221": "Healthcare (Para)", "3212": "Healthcare (Para)",
    "4222": "BPO & Telecalling", "4132": "BPO & Telecalling", "4221": "BPO & Telecalling",
    "5220": "Field Sales & Retail", "5223": "Field Sales & Retail", "3322": "Field Sales & Retail",
    "5244": "Street Vending",
    "9611": "Waste & Recycling", "8344": "Manufacturing",
}

# ── Official salary benchmarks with verified sources ─────────────
OFFICIAL_SALARY_BENCHMARKS = {
    "Plumbing":              {"daily_min": 700,  "daily_max": 1400, "source": "MoSPI PLFS 2022-23"},
    "Electrical Work":       {"daily_min": 800,  "daily_max": 1300, "source": "MoSPI PLFS 2022-23"},
    "Carpentry":             {"daily_min": 700,  "daily_max": 1200, "source": "MoSPI PLFS 2022-23"},
    "AC & Appliance Repair": {"daily_min": 700,  "daily_max": 1400, "source": "MoSPI PLFS 2022-23"},
    "Painting":              {"daily_min": 600,  "daily_max": 1300, "source": "MoSPI PLFS 2022-23"},
    "Masonry":               {"daily_min": 450,  "daily_max": 1200, "source": "MoSPI PLFS 2022-23"},
    "Gig Delivery":          {"mo_min": 12000,   "mo_max": 20000,   "source": "NITI Aayog Gig Economy 2023"},
    "Driver":                {"daily_min": 600,  "daily_max": 1400, "source": "MoSPI PLFS 2022-23"},
    "Domestic (Cleaning)":   {"mo_min": 4000,    "mo_max": 16000,   "source": "ILO India 2023"},
    "Domestic (Cook/Care)":  {"mo_min": 6000,    "mo_max": 18000,   "source": "ILO India 2023"},
    "Food & Hospitality":    {"daily_min": 400,  "daily_max": 1100, "source": "MoSPI PLFS 2022-23"},
    "Agriculture (Crops)":   {"daily_min": 300,  "daily_max": 600,  "source": "NSSO / MoSPI 2022-23"},
    "Agriculture (Livestock)": {"mo_min": 7000,  "mo_max": 14000,   "source": "NSSO / MoSPI 2022-23"},
    "Agriculture (Vendor)":  {"mo_min": 10000,   "mo_max": 18000,   "source": "ILO India 2023"},
    "Apparel & Textile":     {"mo_min": 8000,    "mo_max": 14000,   "source": "NITI Aayog / ILO 2023"},
    "Security & Facility":   {"mo_min": 11000,   "mo_max": 17000,   "source": "PSARA rates 2023"},
    "Manufacturing":         {"mo_min": 12000,   "mo_max": 22000,   "source": "MoSPI PLFS 2022-23"},
    "Beauty & Wellness":     {"daily_min": 500,  "daily_max": 1000, "source": "MoSPI PLFS 2022-23"},
    "Healthcare (Para)":     {"mo_min": 8000,    "mo_max": 40000,   "source": "NHM / MoHFW 2023"},
    "BPO & Telecalling":     {"mo_min": 10000,   "mo_max": 22000,   "source": "NASSCOM 2023"},
    "Field Sales & Retail":  {"mo_min": 10000,   "mo_max": 25000,   "source": "MoSPI PLFS 2022-23"},
    "Street Vending":        {"mo_min": 10000,   "mo_max": 30000,   "source": "ILO India 2023"},
    "Waste & Recycling":     {"mo_min": 6000,    "mo_max": 18000,   "source": "MoSPI PLFS 2022-23"},
}


def salary_from_benchmark(category):
    """Return formatted salary string from official benchmarks."""
    b = OFFICIAL_SALARY_BENCHMARKS.get(category, {})
    if not b:
        return "Not disclosed"
    src = b.get("source", "")
    if "daily_min" in b:
        return f"₹{b['daily_min']}-{b['daily_max']}/day ({src})"
    return f"₹{b['mo_min']}-{b['mo_max']}/mo ({src})"
