"""
WorkMatch Pro v3 — Verification Tests
"""

VERIFY_CASES = [
    ("plumber pipe repair water tap leak bathroom",       "Plumbing",             "Plumber"),
    ("electrician wiring MCB switch fan bijli",           "Electrical Work",      "Electrician"),
    ("mason bricklaying cement wall plaster rajmistri",   "Masonry",              "Mason"),
    ("maid cleaning sweeping jhadu pocha bai",            "Domestic (Cleaning)",  "Maid"),
    ("home cook family meals roti sabzi dal rice",        "Domestic (Cook/Care)", "Cook"),
    ("delivery bike rider Swiggy Zomato gig",             "Gig Delivery",         "Delivery"),
    ("farm worker khet crop harvest field daily wage",    "Agriculture (Crops)",  "Farm"),
    ("tailor darzi stitching blouse kurta silai",         "Apparel & Textile",    "Tailor"),
    ("chowkidar security guard watchman patrol night",    "Security & Facility",  "Security"),
    ("vegetable vendor sabzi thela fruit cart market",    "Agriculture (Vendor)", "Vendor"),
    ("dairy farm cow milk milking Amul doodh",            "Agriculture (Livestock)", "Dairy"),
    ("street food vendor chaat thela hawker cart",        "Street Vending",       "Vendor"),
    ("kabaadi scrap waste picker recycling",              "Waste & Recycling",    "Waste"),
    ("barber naai haircut shave salon trim",              "Beauty & Wellness",    "Barber"),
    ("telecaller outbound calling sales CRM Hindi",       "BPO & Telecalling",    "Telecaller"),
    ("AC repair gas filling compressor cooling HVAC",     "AC & Appliance Repair","AC"),
]


def run_verification(pipeline_fn):
    """Run all verification tests and return accuracy score."""
    print("\n" + "=" * 62)
    print("  🧪  VERIFICATION — Informal Sector Query Tests")
    print("=" * 62)
    passed = 0
    for query, exp_cat, exp_title in VERIFY_CASES:
        rdf, _, _, _ = pipeline_fn(query, "All", "All", "Any Experience", 3)
        if rdf.empty:
            print(f"  ❌ NO RESULTS | {query[:55]}")
            continue
        top = rdf.iloc[0]["Job Title"].lower()
        cat = rdf.iloc[0]["Category"]
        ok = (any(w.lower() in top for w in exp_title.split()) and
              exp_cat.lower() in cat.lower())
        if ok:
            print(f"  ✅ PASS | '{query[:50]}' → {rdf.iloc[0]['Job Title']}")
            passed += 1
        else:
            print(f"  ⚠️  MISS | '{query[:50]}' → got: {rdf.iloc[0]['Job Title']} [{cat}]")
    score = passed / len(VERIFY_CASES) * 100
    print(f"\n  Result: {passed}/{len(VERIFY_CASES)} = {score:.0f}%")
    print("=" * 62)
    return score
