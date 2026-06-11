# AdPulse AI

AdPulse AI is a comprehensive data-analytics and marketing intelligence platform mapping granular ad spend, calculating KPIs (ROAS, CPA, CTR), performing Scikit-Learn/XGBoost predictive forecasting, generating dynamic PDF reports, and leveraging OpenAI to craft natural language executive summaries.

## Features
- **KPI Dashboard**: View real-time SQLite backend data metrics segmented by spend, revenue, clicks, and impressions.
- **Audience Insights**: Break down conversions by device and demographic.
- **Predictive Analytics**: 30-day Machine Learning forecasts on your core metrics.
- **AI Campaign Analyst**: Automatically generate markdown insights analyzing specific demographics and forecasts using GPT-3.5.
- **Automated Reporting**: Export compiled views and AI evaluations natively to Markdown and PDF.

---

## Local Setup Instructions

### 1. Requirements and Environment
Ensure you have Python 3.10+ installed.

```bash
# Clone the repository
git clone <your-repo-url>
cd AdPulseAI

# Create virtual environment
python -m venv venv
# On Windows
.\\venv\\Scripts\\activate
# On Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` into a local `.env` file and insert your active API keys.

```bash
cp .env.example .env
```
Inside `.env`, populate:
`OPENAI_API_KEY=sk-....`

*Note: Without an OpenAI API Key, the platform operates normally but the AI Analyst and Reporting endpoints will return placeholders explicitly notifying you of the missing key.*

### 3. Initialize SQLite Database (Mocking Sample Data)
If you want to view immediate UI without live connections, instantiate mock variables into the SQLAlchemy database structure.

```bash
# Generate the underlying sample CSVs
python generate_sample_data.py

# Fire ETL pipeline routing CSVs -> SQLite representations
python -m etl.load
```

### 4. Boot the Streamlit Application
Start the visual dashboard UI.

```bash
python -m streamlit run app.py
```
Visit http://localhost:8501 inside your browser.

---

## Deploying to Streamlit Cloud

To easily deploy this dashboard securely to the cloud:
1. Push this entire structure to a public/private **GitHub repository**.
2. Navigate to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click "New App", authenticate via GitHub, and select your repository containing AdPulse AI.
4. Set the **Main file path** to `app.py`.
5. Under **Advanced Settings**, declare your environment secrets. Streamlit automatically parses variables entered like standard TOML/dotenv formats:
   ```toml
   OPENAI_API_KEY = "sk-xxxxxxxx"
   ```
6. Click **Deploy!** Streamlit automatically installs packages indicated within `requirements.txt`.

---

## Folder Architecture

```text
AdPulseAI/
├── app.py                   # Streamlit Main Core Application
├── requirements.txt         # Pip dependency list
├── .env.example             # Template for secure keys
├── database/                # SQLite connection mappings and ORMs
├── etl/                     # Extraction, Parsing & SQLite bulk injection rules
├── analytics/               # Group-by segmentation & KPI formula engines
├── ml/                      # XGBoost / RF training pipeline and inference endpoints
├── ai/                      # OpenAI LLM prompt constructor & JSON mappings
├── reports/                 # XHTML2PDF structural HTML parsers & report logic
├── pages/                   # Application modular Streamlit pages UI
├── tests/                   # Python automated unit verification endpoints
├── data/                    # Placeholder tracking for Mock datasets and CSV processing
└── screenshots/             # Storage references for visual documentation previews
```
