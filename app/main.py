from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from artifacts.guestly_recommendation_engine import (
    feature_columns,
    guestly_recommendations,
)


BASE_DIR = Path(__file__).resolve().parent.parent
BOOKING_MODEL_PATH = BASE_DIR / "artifacts" / "abandonment_model.joblib"


@lru_cache(maxsize=1)
def load_booking_model():
    try:
        return joblib.load(BOOKING_MODEL_PATH)
    except Exception:
        return None


app = FastAPI(
    title="Digital Guest Experience AI Service",
    description=(
        "API endpoints for booking abandonment risk predictions "
        "and personalized guest upsell recommendations."
    ),
    version="1.0.0",
)


class BookingRiskRequest(BaseModel):
    Booking_Channel: str = Field(min_length=1)
    Guest_Segment: str = Field(min_length=1)
    Room_Type: str = Field(min_length=1)
    Stay_Length_Days: int = Field(ge=1)
    Nightly_Rate_NGN: float = Field(gt=0)
    Lead_Time_Days: int = Field(ge=0)


class UpsellRequest(BaseModel):
    Guest_Segment: str = Field(min_length=1)
    Room_Type: str = Field(min_length=1)
    Stay_Length_Days: int = Field(ge=1)
    Country: str = Field(min_length=1)
    Airport_Arrival: bool = False
    Spa_Interest: bool = False
    Breakfast_Need: bool = False


@app.get("/health")
def health_check():
    booking_model_available = load_booking_model() is not None

    return {
        "status": "ok",
        "service": "Digital Guest Experience AI Service",
        "models": {
            "booking_risk": (
                "available" if booking_model_available else "unavailable"
            ),
            "upsell_engine": "available",
        },
    }


@app.post("/predict-booking-risk")
def predict_booking_risk(request: BookingRiskRequest):
    model = load_booking_model()

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="The booking risk model is unavailable.",
        )

    input_data = pd.DataFrame(
        [
            {
                "Booking_Channel": request.Booking_Channel,
                "Guest_Segment": request.Guest_Segment,
                "Room_Type": request.Room_Type,
                "Stay_Length_Days": request.Stay_Length_Days,
                "Nightly_Rate_NGN": request.Nightly_Rate_NGN,
                "Lead_Time_Days": request.Lead_Time_Days,
            }
        ]
    )

    try:
        probabilities = model.predict_proba(input_data)[0]
        positive_class_indices = [
            index
            for index, label in enumerate(model.classes_)
            if label == 1
        ]

        if not positive_class_indices:
            raise ValueError("The model does not expose the expected positive class.")

        risk = float(probabilities[positive_class_indices[0]])

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The booking risk prediction could not be completed.",
        )

    if risk >= 0.70:
        risk_level = "high"
        recommended_action = "Prioritize a follow-up with the guest."
    elif risk >= 0.40:
        risk_level = "moderate"
        recommended_action = "Send a booking confirmation reminder."
    else:
        risk_level = "low"
        recommended_action = "Continue with the standard booking process."

    return {
        "status": "success",
        "abandonment_risk": round(risk, 4),
        "risk_level": risk_level,
        "recommended_action": recommended_action,
    }


@app.post("/recommend-upsells")
def recommend_upsells(request: UpsellRequest):
    guest_segment = request.Guest_Segment.strip().lower()
    room_type = request.Room_Type.strip().lower()

    guest_profile = pd.DataFrame(
        [
            {
                "family": int(guest_segment == "family"),
                "long_stay": int(request.Stay_Length_Days >= 3),
                "business": int(guest_segment == "business"),
                "airport_arrival": int(request.Airport_Arrival),
                "spa_interest": int(request.Spa_Interest),
                "breakfast_need": int(request.Breakfast_Need),
                "standard_room": int(room_type == "standard"),
            }
        ],
        columns=feature_columns,
    )

    try:
        recommendations = guestly_recommendations(
            guest_profile,
            top_n=2,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The upsell recommendations could not be generated.",
        )

    recommended_services = recommendations.to_dict(orient="records")

    for service in recommended_services:
        service["similarity_score"] = float(service["similarity_score"])

    return {
        "status": "success",
        "recommended_services": recommended_services,
    }
