# Digital-Guest-Experience-AM.
AI/ML components for a Digital Guest Experience Platform.
# Digital Guest Experience Platform — AI/ML Microservice

## Setup
1. Clone repo: `git clone https://github.com/chinwenduanoziea-art/Digital-Guest-Experience-AI-ML.git`
2. Create & activate venv: `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`

## Where Each Member Puts Their Files
- **Member 1:** Save `01_booking_risk.ipynb` in `notebooks/` and `abandonment_model.joblib` in `artifacts/`
- **Member 2:** Save `02_upsell_engine.ipynb` in `notebooks/` and `upsell_model.joblib` in `artifacts/`
- **Member 3:** Save `03_concierge_router.ipynb` in `notebooks/` and `concierge_model.joblib` in `artifacts/`
- **Member 4:** Save `main.py` in `app/`
- **Member 5:** Runs `pytest -v` and verifies `uvicorn app.main:app --reload`

## API Endpoints (For Backend Team)
Start server: `uvicorn app.main:app --reload --port 8000`
Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

- `POST /predict-booking-risk` — Predicts booking abandonment/cancellation probability before Paystack checkout.
- `POST /recommend-upsells` — Returns top 2 personalized extra services for a guest profile.
- `POST /route-concierge` — Routes guest chat text to the right hotel department and flags SLA risks.