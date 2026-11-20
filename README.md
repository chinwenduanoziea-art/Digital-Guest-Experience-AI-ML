# Digital Guest Experience Platform - AI/ML Microservice

An end-to-end AI/ML and FastAPI microservice powering intelligent guest experience workflows across booking retention, personalized upsells, and guest service resolution benchmarking.

## Project Architecture & Repository Structure

- **app/main.py**: FastAPI application & inference endpoints (Member 4)
- **artifacts/abandonment_model.joblib**: Task 1 trained RandomForest booking risk pipeline
- **artifacts/guestly_recommendation_engine.py**: Task 2 content-based cosine similarity upsell engine
- **data/**: Cleaned and raw hospitality datasets and evaluation outputs
- **notebooks/01_booking_risk.ipynb**: Task 1 booking abandonment risk modeling & evaluation
- **notebooks/03_resolution_time_prediction.ipynb**: Task 3 guest service resolution time benchmarking
- **notebooks/guestly_upsell_engine.ipynb** (+ cont1, cont2, summary): Task 2 upsell modeling notebooks
- **tests/test_api.py**: Automated FastAPI endpoint verification suite

## AI/ML Components & Deliverables

1. **Task 1 - Booking Abandonment & Cancellation Risk** (
otebooks/01_booking_risk.ipynb & rtifacts/abandonment_model.joblib)
   - **Model:** scikit-learn Pipeline (OneHotEncoder + StandardScaler + RandomForestClassifier).
   - **Performance:** 0.7824 validation accuracy and 0.8446 ROC-AUC on hotel_bookings_cleaned.csv.
   - **Endpoint:** POST /predict-booking-risk - accepts Booking_Channel, Guest_Segment, Room_Type, Stay_Length_Days, Nightly_Rate_NGN, and Lead_Time_Days; returns abandonment_risk (0.0-1.0) and recommended_action.

2. **Task 2 - Personalized Upsell Recommendation Engine** (rtifacts/guestly_recommendation_engine.py)
   - **Model:** Content-based cosine similarity recommendation engine scoring guest stay profiles against hospitality add-on packages with human-readable explanations.
   - **Endpoint:** POST /recommend-upsells - accepts Guest_Segment, Room_Type, Stay_Length_Days, and Country; returns the top 2 personalized extra services (recommended_services).

3. **Task 3 - Guest Service Resolution Time Prediction** (
otebooks/03_resolution_time_prediction.ipynb)
   - **Research Finding:** Benchmarking demonstrated that stratified baseline averages outperform complex tree and linear regressors on noisy service ticket logs. Documented as an exploratory notebook with aggregate evaluation metrics (no .joblib artifact or live prediction endpoint required).

4. **Task 4 - FastAPI Backend Integration** (pp/main.py - Member 4)
   - Implements GET /health, POST /predict-booking-risk, and POST /recommend-upsells using the artifacts in artifacts/.

5. **Task 5 - QA & Repository Verification** (	ests/test_api.py - Member 5)
   - Verifies repository structure, artifact integrity, server startup, and end-to-end API responses via pytest -v.

## Local Setup & Running Tests

1. Clone repo: git clone https://github.com/chinwenduanoziea-art/Digital-Guest-Experience-AI-ML.git
2. Activate venv: python -m venv .venv && .\.venv\Scripts\Activate.ps1
3. Install dependencies: pip install -r requirements.txt
4. Start API server: uvicorn app.main:app --reload --port 8000
5. Run automated tests: python -m pytest -v


Summary of My Task 4 – FastAPI Microservice
I implemented the FastAPI microservice to make the existing booking-risk model and personalized upsell engine accessible through JSON endpoints.
I added three endpoints:
1. GET /health – checks service and model availability.
2. POST /predict-booking-risk – predicts booking abandonment risk and suggests an action.
3. POST /recommend-upsells – returns personalized service recommendations with explanations and similarity scores.
I also added input validation, error handling and a dedicated GitHub Actions workflow with API tests.
The GitHub Actions workflow ran successfully, and all Task 4 checks passed.
The implementation is ready for QA and backend integration.
Soft Nation Dev