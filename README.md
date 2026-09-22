# Disneyland Magic Key Breakeven Calculator

A small Dash web app for comparing Disneyland Magic Key pass costs against the cost of buying single-day tickets, parking, and food/merch for different group scenarios.

## What it does

- Lets you adjust global assumptions like ticket cost, parking, and food/merch spend
- Configures the major Magic Key tiers (Inspire, Believe, Explore, Imagine)
- Builds comparison scenarios for groups with multiple pass types and vehicle counts
- Shows cumulative cost comparison charts and breakeven calculations
- Displays individual pass breakeven metrics for each tier

## Tech stack

- Python
- Dash
- Dash Bootstrap Components
- Plotly

## Local setup

1. Open the project folder
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install dash dash-bootstrap-components plotly
```

4. Run the app:

```bash
python app.py
```

5. Open the URL shown in the terminal, typically:

```text
http://127.0.0.1:8050
```

## Notes

This app is intended for estimating whether a Magic Key is worth it for a given travel pattern or family/group scenario. It is a planning tool and not an official Disney pricing calculator.
