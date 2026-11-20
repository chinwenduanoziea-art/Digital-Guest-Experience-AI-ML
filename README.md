# Digital Guest Experience Platform - AI/ML Microservice

This project brings together the AI/ML work for the Digital Guest Experience platform. It currently covers booking abandonment risk and personalized upsell recommendations, with the service-resolution research documented separately.

## Project structure

- `app/main.py`: FastAPI application and prediction endpoints.
- `artifacts/abandonment_model.joblib`: trained booking-risk pipeline.
- `artifacts/guestly_recommendation_engine.py`: personalized upsell recommendation logic.
- `data/`: project datasets and evaluation outputs.
- `notebooks/`: model development and evaluation notebooks.
- `tests/test_api.py`: API checks maintained as part of the project QA work.

## What the API provides

The API makes the available booking-risk model and upsell recommendation engine accessible to the backend through JSON requests and responses.

### Health check

`GET /health`

Returns the service status and whether the booking-risk model and upsell engine are available.

### Booking risk

`POST /predict-booking-risk`

Send the booking details below:

```json
{
  "Booking_Channel": "Website",
  "Guest_Segment": "Solo",
  "Room_Type": "Standard",
  "Stay_Length_Days": 3,
  "Nightly_Rate_NGN": 45000,
  "Lead_Time_Days": 30
}
```

The response includes the predicted abandonment risk, a risk level, and a suggested follow-up action.

### Personalized upsells

`POST /recommend-upsells`

Send the guest details below:

```json
{
  "Guest_Segment": "Couple",
  "Room_Type": "Suite",
  "Stay_Length_Days": 4,
  "Country": "UK"
}
```

The response returns up to two recommended services with their similarity scores and explanations. The request also accepts optional boolean fields: `Airport_Arrival`, `Spa_Interest`, and `Breakfast_Need`.

The current recommendation engine uses the guest segment, length of stay, room type, and optional interest signals to build its recommendation profile. `Country` is accepted in the request for backend compatibility, but it is not currently used in the recommendation score.

## A note on the available models

The booking-risk endpoint loads the trained pipeline from `artifacts/abandonment_model.joblib`. The upsell endpoint calls the existing recommendation engine in `artifacts/guestly_recommendation_engine.py`.

Task 3 is currently documented as an exploratory service-resolution-time experiment. Its notebook does not produce a deployable model artifact, so there is no concierge or resolution-time prediction endpoint in this API at this stage.

## Run locally

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Once it is running, the interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

The existing automated checks can be run with `python -m pytest -v`. API QA and final backend handoff remain with the project QA lead.
