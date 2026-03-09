# ⚡ WorkMatch Pro v4 — India Informal Sector Job Matcher (Live Data)

> AI-powered job matching for India's 500M+ informal workers.
> Uses **SBERT + CNN + spaCy + RapidFuzz** with **live data** from Adzuna, eShram, and OGD India.

---

## 🌐 Live Data Sources

| #   | Source                                            | What It Provides                          | Auth             |
| --- | ------------------------------------------------- | ----------------------------------------- | ---------------- |
| 1   | [Adzuna India API](https://developer.adzuna.com/) | Real-time job vacancies                   | Free API key     |
| 2   | [eShram Dashboard](https://eshram.gov.in)         | Live worker registration counts by sector | Public           |
| 3   | [OGD data.gov.in](https://data.gov.in)            | eShram + PLFS official statistics         | Optional API key |
| 4   | [NCS Portal](https://ncs.gov.in)                  | Government vacancy data                   | Public           |
| 5   | MoSPI PLFS 2022-23                                | Official salary benchmarks                | Built-in         |

All data is cached for 6 hours. The app works fully offline with seed data if no API keys are set.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** ([download](https://python.org))
- ~4 GB disk space (for ML models)

### Option 1: One-Click Run

**Windows:**

```bash
run.bat
```

**Linux / Mac:**

```bash
chmod +x run.sh && ./run.sh
```

### Option 2: Manual Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/workmatch-pro.git
cd workmatch-pro

# Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# (Optional) Set up API keys
cp .env.example .env
# Edit .env with your Adzuna + OGD keys

# Run the app
python app.py
```

---

## 🔑 API Keys (Optional but Recommended)

Create a `.env` file (or copy `.env.example`):

```env
ADZUNA_APP_ID=your_id          # Free at https://developer.adzuna.com/
ADZUNA_APP_KEY=your_key
DATA_GOV_API_KEY=your_key      # Free at https://data.gov.in/user/register
```

Without keys: runs on 170+ NCO-verified seed jobs.
With keys: fetches 200+ live jobs from Adzuna India on every startup.

---

## 📁 Project Structure

```
workmatch-pro/
├── app.py                 # Main entry point
├── config.py              # Constants, API keys, .env loader
├── styles.py              # Gradio CSS & category colors
├── salary_benchmarks.py   # Official salary data + NCO/eShram maps
├── live_data.py           # Adzuna, eShram, OGD, NCS, PLFS fetchers
├── data_loader.py         # Combines seed data into DataFrame
├── database.py            # SQLite operations (seed + live)
├── ai_engine.py           # SBERT + CNN + spaCy + RapidFuzz
├── training_pairs.py      # 69 CNN training pairs
├── pipeline.py            # Matching pipeline with 7 filters
├── verification.py        # 16 accuracy test cases
├── ui.py                  # Gradio web interface
├── seed_construction.py   # Jobs: Plumbing, Electrical, Carpentry, AC, Painting, Masonry
├── seed_services.py       # Jobs: Delivery, Driver, Domestic, Food, Agriculture
├── seed_urban.py          # Jobs: Apparel, Security, Manufacturing, Beauty, Healthcare, BPO, Sales, Vending, Waste
├── requirements.txt       # Python dependencies
├── .env.example           # API key template
├── .gitignore             # Git ignore rules
├── run.bat                # Windows quick start
└── run.sh                 # Linux/Mac quick start
```

---

## 📊 Categories (22 — All Informal)

| #   | Category                | Sector         | Example Jobs                           |
| --- | ----------------------- | -------------- | -------------------------------------- |
| 1   | Plumbing                | Construction   | Plumber, Drainage, Water Tanker        |
| 2   | Electrical Work         | Construction   | Electrician, Lineman, Solar            |
| 3   | Carpentry               | Construction   | Carpenter, Shuttering, Modular Kitchen |
| 4   | AC & Appliance Repair   | Electronics    | AC Tech, Mobile Repair, CCTV           |
| 5   | Painting                | Construction   | House Painter, Waterproofing           |
| 6   | Masonry                 | Construction   | Mason, Mazdoor, Welder, Tile Fixer     |
| 7   | Gig Delivery            | Transport      | Swiggy, Zomato, Blinkit, Amazon Flex   |
| 8   | Driver                  | Transport      | Ola/Uber, Truck, Auto, School Van      |
| 9   | Domestic (Cleaning)     | Domestic       | Part-time Maid, Live-in, Deep Clean    |
| 10  | Domestic (Cook/Care)    | Domestic       | Home Cook, Babysitter, Elder Care      |
| 11  | Food & Hospitality      | Hospitality    | Restaurant Cook, Dhaba, Waiter         |
| 12  | Agriculture (Crops)     | Agriculture    | Farm Worker, Tractor, Irrigation       |
| 13  | Agriculture (Livestock) | Agriculture    | Dairy, Poultry, Fishing                |
| 14  | Agriculture (Vendor)    | Agriculture    | Sabzi Vendor, Fish Seller              |
| 15  | Apparel & Textile       | Apparel        | Tailor, Garment Factory, Embroidery    |
| 16  | Security & Facility     | Security       | Guard, Office Boy, Housekeeping        |
| 17  | Manufacturing           | Manufacturing  | CNC Operator, Fitter, QC, Packing      |
| 18  | Beauty & Wellness       | Wellness       | Barber, Beautician, Mehndi Artist      |
| 19  | Healthcare (Para)       | Healthcare     | Nurse, ANM, ASHA, Lab Tech             |
| 20  | BPO & Telecalling       | ITES           | Telecaller, Data Entry, Customer Care  |
| 21  | Field Sales & Retail    | Retail         | FMCG Sales, Insurance, Kirana          |
| 22  | Street Vending          | Informal Trade | Chaat Vendor, Fruit Cart, Paan Shop    |
| 23  | Waste & Recycling       | Waste Mgmt     | Ragpicker, Sanitation, Scrap Dealer    |

---

## 🛠️ Tech Stack

| Component   | Technology                                      |
| ----------- | ----------------------------------------------- |
| Embeddings  | Sentence-Transformers `all-MiniLM-L6-v2` (384D) |
| Classifier  | TensorFlow/Keras CNN                            |
| NLP         | spaCy `en_core_web_sm`                          |
| Fuzzy Match | RapidFuzz                                       |
| Live Jobs   | Adzuna India API                                |
| Live Stats  | eShram + OGD + NCS + PLFS                       |
| UI          | Gradio 4.44 (dark theme)                        |
| Database    | SQLite                                          |
| Caching     | cachetools (6h TTL)                             |

---

## 📝 License

MIT License. Free to use, modify, and distribute.
