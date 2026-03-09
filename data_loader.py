"""
WorkMatch Pro v4 — Data Loader
Combines all seed modules into a single DataFrame with v4 source citations.
"""

import re
import pandas as pd

from seed_construction import PLUMBING, ELECTRICAL, CARPENTRY, AC_APPLIANCE, PAINTING, MASONRY
from seed_services import (GIG_DELIVERY, DRIVER, DOMESTIC_CLEANING, DOMESTIC_COOKCARE,
                           FOOD_HOSPITALITY, AGRICULTURE_CROPS, AGRICULTURE_LIVESTOCK,
                           AGRICULTURE_VENDOR)
from seed_urban import (APPAREL, SECURITY, MANUFACTURING, BEAUTY, HEALTHCARE,
                        BPO, FIELD_SALES, STREET_VENDING, WASTE)


def sal_to_monthly(s):
    """Convert any salary string to rough monthly equivalent."""
    s = str(s).lower()
    nums = re.findall(r'[\d]+', s)
    if not nums:
        return 0
    n = int(nums[0])
    if "lpa" in s:
        return int(n * 100000 / 12)
    if "/day" in s or "day" in s:
        return n * 26
    if "/delivery" in s:
        return n * 300
    return n


def load_seed_data():
    """Load and combine all seed data into a single DataFrame."""
    RAW_SEED = (PLUMBING + ELECTRICAL + CARPENTRY + AC_APPLIANCE + PAINTING + MASONRY +
                GIG_DELIVERY + DRIVER + DOMESTIC_CLEANING + DOMESTIC_COOKCARE +
                FOOD_HOSPITALITY + AGRICULTURE_CROPS + AGRICULTURE_LIVESTOCK +
                AGRICULTURE_VENDOR + APPAREL + SECURITY + MANUFACTURING + BEAUTY +
                HEALTHCARE + BPO + FIELD_SALES + STREET_VENDING + WASTE)

    df = pd.DataFrame(RAW_SEED)
    df["description"] = df["skills"]
    df["source"] = "seed_eshram_nco_v4_verified"
    df["live_url"] = ""
    df["posted_date"] = ""
    df["salary_min_mo"] = df["sal"].apply(sal_to_monthly)
    df = df.rename(columns={
        "nco": "nco_code", "sector": "nco_sector", "cat": "category",
        "loc": "location", "sal": "salary", "sal_type": "salary_type",
        "edu": "min_education", "exp": "experience", "co": "company",
        "vehicle": "vehicle_owned",
    })
    return df
