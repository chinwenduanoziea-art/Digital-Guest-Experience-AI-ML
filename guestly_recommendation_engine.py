
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

feature_columns = [
    "family", "long_stay", "business",
    "airport_arrival", "spa_interest",
    "breakfast_need", "standard_room"
]

service_features = pd.DataFrame({
    "service_name": [
        "Breakfast Package", "Airport Pickup",
        "Spa Package", "Late Checkout",
        "Room Upgrade", "Laundry Service",
        "Family Package"
    ],
    "family": [1,0,0,0,0,0,1],
    "long_stay": [1,0,0,1,0,1,1],
    "business": [0,1,0,1,1,0,0],
    "airport_arrival": [0,1,0,0,0,0,0],
    "spa_interest": [0,0,1,0,0,0,0],
    "breakfast_need": [1,0,0,0,0,0,1],
    "standard_room": [0,0,0,0,1,0,0]
})

def recommend_for_guest(guest_profile, top_n=3):
    scores = cosine_similarity(
        guest_profile[feature_columns],
        service_features[feature_columns]
    )[0]

    results = pd.DataFrame({
        "service_name": service_features["service_name"],
        "similarity_score": scores
    })

    results = results[results["similarity_score"] > 0]
    results = results.sort_values(
        "similarity_score", ascending=False
    )

    return results.head(top_n).reset_index(drop=True)

def explain_recommendation(service_name, guest):
    explanations = {
        "Breakfast Package": "Additional breakfast option may be useful.",
        "Airport Pickup": "Convenient airport transportation.",
        "Spa Package": "Matches the recorded wellness interest.",
        "Late Checkout": "Provides additional checkout flexibility.",
        "Room Upgrade": "An upgrade may suit the guest's room preferences.",
        "Laundry Service": "Useful for guests staying longer.",
        "Family Package": "Suitable for guests travelling with children."
    }

    return explanations.get(service_name, "Matches guest profile.")

def guestly_recommendations(guest_profile, top_n=3):
    recommendations = recommend_for_guest(guest_profile, top_n)

    recommendations["reason"] = recommendations["service_name"].apply(
        lambda service: explain_recommendation(service, guest_profile)
    )

    return recommendations

def guestly_api_recommendation(guest_profile):
    recommendations = guestly_recommendations(guest_profile)

    return {
        "status": "success",
        "recommendations": recommendations.to_dict(orient="records")
    }
