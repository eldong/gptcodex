# Minimal FastAPI Currency Converter

A tiny FastAPI web app that converts U.S. Dollars (USD) to Euros (EUR) or Indian Rupees (INR) using an in-code exchange rate table. Logic lives in a dedicated services layer and the API stays in its own module, following project conventions.

## User Stories
- **US1**: As a visitor, I want to enter an amount in USD so I can convert it to another currency.
- **US2**: As a visitor, I want to choose between EUR or INR so I can see the amount in my target currency.
- **US3**: As a visitor, I want to be notified when my input is invalid so I can correct it quickly.

## Acceptance Criteria
- **AC1**: Given a positive USD amount and the EUR option, the app displays the EUR value using the embedded EUR rate with two decimal places.
- **AC2**: Given a positive USD amount and the INR option, the app displays the INR value using the embedded INR rate with two decimal places.
- **AC3**: Given an empty, negative, or non-numeric amount, the app does not attempt conversion and surfaces a clear validation message.
- **AC4**: Currency options are limited to EUR and INR, and the UI reflects the currently selected option.
- **AC5**: Exchange rates are sourced exclusively from the in-code table; no external API calls are made.

## Minimal File Structure
```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main.py
│   ├── services
│   │   ├── __init__.py
│   │   └── conversion.py
│   └── templates
│       └── index.html
├── tests
│   └── test_conversion.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Local Environment
1. Create the virtual environment (already initialized once):
   ```powershell
   python -m venv .venv
   ```
2. Activate it:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - cmd: `\venv\Scripts\activate.bat`
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running & Testing
- Start the dev server: `uvicorn app.main:app --reload`
- Open the form at http://127.0.0.1:8000/
- Run tests: `pytest`
