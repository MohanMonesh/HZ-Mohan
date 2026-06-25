# Election Results Publishing Portal™

Enterprise-grade Streamlit platform for real-time election result publishing, historical analytics, and machine-readable public data access.

## Features

- **Executive Dashboard** — Live KPIs, progress indicators, auto-refresh
- **Role-Based Authentication** — Super Admin, Election Officer, Analyst, Public User
- **Excel/CSV Import** — Drag-and-drop with downloadable templates
- **Data Validation Engine** — Automated integrity checks
- **Live Results** — Searchable, sortable, paginated result tables
- **Historical Comparison** — Swing analysis, turnout trends, Sankey diagrams
- **Geographic Maps** — Plotly and Folium interactive visualizations
- **AI Insights** — Automated trend detection and insight cards
- **Reports & Exports** — PDF, Excel, CSV, JSON
- **Alerts Center** — Margin warnings, declaration notifications
- **Dark/Light Theme** — Glassmorphism enterprise UI

## Quick Start

```bash
cd election-results-portal
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python utils/seed_data.py    # Optional — app auto-seeds on first run
streamlit run app.py
```

Open **http://localhost:8501**

## Demo Accounts

| Username | Password     | Role             |
|----------|--------------|------------------|
| admin    | Admin@2024   | Super Admin      |
| officer  | Officer@2024 | Election Officer |
| analyst  | Analyst@2024 | Analyst          |
| public   | Public@2024  | Public User      |

## Logo

Place your company logo at `assets/logo.png` (or `.jpg`). The app derives theme colors from it automatically. A default SVG logo is included.

## Project Structure

```
election-results-portal/
├── app.py                 # Main entry point
├── assets/logo.svg        # Brand logo
├── config/settings.py     # Configuration
├── core/                  # Auth, database, theme
├── services/              # Business logic
├── pages/                 # UI page modules
├── components/            # Reusable UI components
├── utils/seed_data.py     # Sample data seeder
└── data/                  # SQLite DB & exports
```

## Technology Stack

Streamlit · Pandas · Plotly · Folium · AgGrid · ReportLab · SQLite (PostgreSQL-ready)

## License

Proprietary — Election Results Publishing Portal™
