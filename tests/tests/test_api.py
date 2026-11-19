from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_booking_risk():
    payload = {
        "Booking_Channel": "Website",
        "Guest_Segment": "Solo",
        "Room_Type": "Standard",
        "Stay_Length_Days": 3,
        "Nightly_Rate_NGN": 45000.0,
        "Lead_Time_Days": 30,
    }
    response = client.post("/predict-booking-risk", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert 0.0 <= body["abandonment_risk"] <= 1.0
    assert "recommended_action" in body


def test_recommend_upsells():
    payload = {
        "Guest_Segment": "Couple",
        "Room_Type": "Suite",
        "Stay_Length_Days": 4,
        "Country": "UK",
    }
    response = client.post("/recommend-upsells", json=payload)
    assert response.status_code == 200
    assert len(response.json()["recommended_services"]) == 2


def test_route_concierge():
    payload = {"message": "Please send someone to clean my room"}
    response = client.post("/route-concierge", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["department"] == "Housekeeping"
    assert body["priority"] == "HIGH_SLA_RISK"