# ☄️ Near-Earth Asteroid Explorer

A data exploration and AI-assisted analytics project built using NASA Near-Earth Object (NEO) data.

This project started as a way to learn more about asteroid observations and slowly turned into something bigger for me: an ETL pipeline, an interactive dashboard, and an experiment in combining structured data analysis with LLM-powered exploration.

---

## Features

- Extract asteroid observations directly from the NASA NEO API
- Build and maintain a historical dataset over time
- Clean, transform, and deduplicate observations
- Explore data through an interactive Streamlit interface
- Generate statistical summaries and KPI-style metrics
- Ask questions using OpenAI-powered natural language analysis

---

## Dataset Snapshot

Current dataset:

- 451 total observations
- 449 unique near-Earth asteroids
- 36 potentially hazardous asteroids
- Hazard rate: ~8.0%
- Date coverage: February 2025 → May 2026

Observations may contain repeat measurements across dates; unique asteroid counts are deduplicated using NASA object IDs.

Source: NASA Near-Earth Object API

---

## Project Structure

```text
Near-Earth-Asteroid-Explorer/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── neos.csv
│
├── notebooks/
│   └── neo_exploration.ipynb
│
└── src/
    └── fetch_data.py
```

---

## Pipeline

```text
NASA API
↓
Extract
↓
Transform (clean + flatten JSON)
↓
Load (historical CSV)
↓
Interactive dashboard
↓
AI-assisted exploration
```

This project follows an ETL-style workflow.

### Extract

Retrieve asteroid observations from the NASA API.

### Transform

- Flatten nested JSON responses
- Convert and standardize data types
- Remove duplicate observations
- Generate structured analytical datasets

### Load

Store processed observations for downstream analysis and dashboard usage.

---

## Setup

Clone the repository:

```bash
git clone https://github.com/lollichtalia/Asteroid-Data-Analysis.git
cd Asteroid-Data-Analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configure API Keys

API keys are stored using environment variables instead of hardcoding credentials.

### NASA API

Generate a NASA API key and set it locally.

Mac/Linux:

```bash
export NASA_API_KEY="your_key_here"
```

Windows (PowerShell):

```powershell
$env:NASA_API_KEY="your_key_here"
```

---

### OpenAI API (Optional)

Enable AI-assisted exploration.

Mac/Linux:

```bash
export OPENAI_API_KEY="your_key_here"
```

Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

---

## Export Historical NASA Data

Collect asteroid observations for custom date ranges.

Example:

```bash
python src/fetch_data.py --start 2026-01-01 --days 30
```

Another example:

```bash
python src/fetch_data.py --start 2025-02-23 --days 365
```

Data is automatically:

- downloaded
- transformed
- appended
- deduplicated

Output:

```text
data/neos.csv
```

---

## Run the Dashboard

Launch the application:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Example Questions

Try asking:

- What patterns stand out in this dataset?
- What percentage of observed asteroids are hazardous?
- What characteristics distinguish hazardous asteroids?
- Compare hazardous and non-hazardous observations.
- Which observations deserve further investigation?
- If you were presenting this dataset, what KPIs would you track?

---

## Findings

A few observations from exploratory analysis:

- Hazardous asteroids represented approximately 8% of observations
- Hazardous asteroids appeared larger on average than non-hazardous asteroids
- Hazardous asteroids also showed higher average velocities
- Miss distance alone did not appear to explain hazard classification

These findings describe this dataset only and are not predictive.

---

## AI Integration

This application integrates OpenAI APIs to support:

- Natural language querying
- Statistical interpretation
- Conversational exploration
- Dataset summarization

One design lesson from development:

LLMs perform better when interpreting computed statistics rather than calculating them directly.

The application computes dataset metrics in Python and uses the LLM for explanation rather than statistical calculation.

---

## Tech Stack

Python  
Pandas  
Streamlit  
OpenAI API  
Requests  
Jupyter Notebook  

---

## Future Work

- Add historical trend tracking
- Improve dashboard interactivity
- Add visual comparisons and reporting
- Explore anomaly detection methods
- Investigate interesting asteroid candidates individually

---

Built because space is cool and data tells stories.