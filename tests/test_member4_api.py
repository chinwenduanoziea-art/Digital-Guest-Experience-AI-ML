from fastapi.testclient import TestClient

from app.main import app, load_booking_model


client = TestClient(app)


def test_health_reports_available_components():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["models"]["booking_risk"] == "available"
    assert body["models"]["upsell_engine"] == "available"


def test_booking_risk_endpoint_returns_prediction():
    assert load_booking_model() is not None

    response = client.post(
        "/predict-booking-risk",
        json={
            "Booking_Channel": "Website",
            "Guest_Segment": "Solo",
            "Room_Type": "Standard",
            "Stay_Length_Days": 3,
            "Nightly_Rate_NGN": 45000,
            "Lead_Time_Days": 30,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert 0 <= body["abandonment_risk"] <= 1
    assert body["risk_level"] in {"low", "moderate", "high"}
    assert body["recommended_action"]


def test_upsell_endpoint_returns_recommendations():
    response = client.post(
        "/recommend-upsells",
        json={
            "Guest_Segment": "Couple",
            "Room_Type": "Suite",
            "Stay_Length_Days": 4,
            "Country": "UK",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert len(body["recommended_services"]) == 2
    for service in body["recommended_services"]:
        assert service["service_name"]
        assert service["reason"]
        assert 0 <= service["similarity_score"] <= 1


def test_booking_endpoint_rejects_invalid_input():
    response = client.post(
        "/predict-booking-risk",
        json={
            "Booking_Channel": "Website",
            "Guest_Segment": "Solo",
            "Room_Type": "Standard",
            "Stay_Length_Days": 0,
            "Nightly_Rate_NGN": 45000,
            "Lead_Time_Days": 30,
        },
    )

    assert response.status_code == 422


def test_upsell_endpoint_rejects_invalid_input():
    response = client.post(
        "/recommend-upsells",
        json={
            "Guest_Segment": "Couple",
            "Room_Type": "Suite",
            "Stay_Length_Days": 0,
            "Country": "UK",
        },
    )

    assert response.status_code == 422
