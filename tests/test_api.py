from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["models"]["upsell_engine"] == "available"


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
    assert body["status"] == "success"
    assert 0.0 <= body["abandonment_risk"] <= 1.0
    assert body["risk_level"] in {"low", "moderate", "high"}
    assert "recommended_action" in body


def test_booking_risk_rejects_invalid_input():
    payload = {
        "Booking_Channel": "Website",
        "Guest_Segment": "Solo",
        "Room_Type": "Standard",
        "Stay_Length_Days": 0,
        "Nightly_Rate_NGN": 45000.0,
        "Lead_Time_Days": 30,
    }

    response = client.post("/predict-booking-risk", json=payload)

    assert response.status_code == 422


def test_recommend_upsells():
    payload = {
        "Guest_Segment": "Couple",
        "Room_Type": "Suite",
        "Stay_Length_Days": 4,
        "Country": "UK",
    }

    response = client.post("/recommend-upsells", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert len(body["recommended_services"]) == 2
    assert all(
        "service_name" in service and "reason" in service
        for service in body["recommended_services"]
    )


def test_upsell_rejects_invalid_input():
    payload = {
        "Guest_Segment": "Couple",
        "Room_Type": "Suite",
        "Stay_Length_Days": 0,
        "Country": "UK",
    }

    response = client.post("/recommend-upsells", json=payload)

    assert response.status_code == 422
