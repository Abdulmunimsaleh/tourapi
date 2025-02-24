from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from rapidfuzz import process

app = FastAPI()

# Sample tour data
TOUR_DATA = {
     "Kenya": {
        "January": [
            {"tour_name": "Masai Mara Safari", "duration": 3, "price_per_person": 500, "highlights": ["Big Five", "Game Drives"], "destination": "Masai Mara", "dates": ["15th - 20th January"]},
            {"tour_name": "Amboseli Adventure", "duration": 2, "price_per_person": 400, "highlights": ["Mount Kilimanjaro", "Elephants"], "destination": "Amboseli National Park", "dates": ["22nd - 25th January"]}
        ],
        "February": [
            {"tour_name": "Lake Nakuru & Naivasha Tour", "duration": 2, "price_per_person": 350, "highlights": ["Flamingos", "Boat Rides"], "destination": "Lake Nakuru", "dates": ["5th - 7th February"]},
            {"tour_name": "Tsavo National Park Safari", "duration": 3, "price_per_person": 450, "highlights": ["Lions", "Red Elephants"], "destination": "Tsavo National Park", "dates": ["18th - 21st February"]}
        ],
        "March": [
            {"tour_name": "Nairobi National Park Day Tour", "duration": 1, "price_per_person": 200, "highlights": ["Urban Safari", "Giraffe Center"], "destination": "Nairobi National Park", "dates": ["3rd - 3rd March"]},
            {"tour_name": "Diani Beach Relaxation", "duration": 4, "price_per_person": 600, "highlights": ["Beach Experience", "Water Sports"], "destination": "Diani Beach", "dates": ["12th - 16th March"]}
        ]
    },
    "Tanzania": {
        "January": [
            {"tour_name": "Serengeti Safari", "duration": 4, "price_per_person": 800, "highlights": ["Great Migration", "Game Drives"], "destination": "Serengeti National Park", "dates": ["10th - 15th January"]},
            {"tour_name": "Mount Kilimanjaro Trek", "duration": 7, "price_per_person": 1500, "highlights": ["Climbing", "Scenic Views"], "destination": "Mount Kilimanjaro", "dates": ["20th - 30th January"]}
        ],
        "February": [
            {"tour_name": "Zanzibar Beach Holiday", "duration": 5, "price_per_person": 900, "highlights": ["White Sand Beaches", "Dolphin Tours"], "destination": "Zanzibar", "dates": ["7th - 12th February"]},
            {"tour_name": "Ngorongoro Crater Safari", "duration": 3, "price_per_person": 750, "highlights": ["Wildlife Spotting", "Crater Views"], "destination": "Ngorongoro Crater", "dates": ["19th - 22nd February"]}
        ],
        "March": [
            {"tour_name": "Tarangire National Park Safari", "duration": 2, "price_per_person": 500, "highlights": ["Elephants", "Baobab Trees"], "destination": "Tarangire National Park", "dates": ["2nd - 4th March"]},
            {"tour_name": "Mikumi National Park Safari", "duration": 3, "price_per_person": 600, "highlights": ["Lions", "Scenic Safari"], "destination": "Mikumi National Park", "dates": ["15th - 18th March"]}
        ]
    },
    "South Africa": {
        "January": [
            {"tour_name": "Kruger National Park Safari", "duration": 3, "price_per_person": 700, "highlights": ["Big Five", "Luxury Lodges"], "destination": "Kruger National Park", "dates": ["8th - 12th January"]},
            {"tour_name": "Cape Town & Table Mountain", "duration": 2, "price_per_person": 500, "highlights": ["Cable Car", "Wine Tasting"], "destination": "Cape Town", "dates": ["15th - 17th January"]}
        ],
        "February": [
            {"tour_name": "Garden Route Adventure", "duration": 5, "price_per_person": 900, "highlights": ["Scenic Views", "Wildlife"], "destination": "Garden Route", "dates": ["9th - 14th February"]},
            {"tour_name": "Johannesburg & Soweto Tour", "duration": 1, "price_per_person": 250, "highlights": ["Apartheid Museum", "History"], "destination": "Johannesburg", "dates": ["20th - 20th February"]}
        ],
        "March": [
            {"tour_name": "Victoria Falls & Zambezi River", "duration": 3, "price_per_person": 800, "highlights": ["Waterfalls", "River Cruise"], "destination": "Victoria Falls", "dates": ["5th - 8th March"]},
            {"tour_name": "Drakensberg Mountains Hike", "duration": 4, "price_per_person": 600, "highlights": ["Scenic Trails", "Nature"], "destination": "Drakensberg Mountains", "dates": ["22nd - 26th March"]}
        ]
    }
    
}

# Normalize keys to lowercase
TOUR_DATA = {k.lower(): {m.lower(): v for m, v in v.items()} for k, v in TOUR_DATA.items()}

# List of valid countries and months in lowercase
VALID_COUNTRIES = list(TOUR_DATA.keys())
VALID_MONTHS = list(set(month for country in TOUR_DATA.values() for month in country.keys()))

class TourRequest(BaseModel):
    country: str
    month: str

def get_best_match(user_input: str, choices: list, threshold: int = 80):
    """Find the closest match for user input in a list of valid choices."""
    user_input = user_input.lower()
    match, score, _ = process.extractOne(user_input, choices)
    return match if score >= threshold else None

@app.get("/tours")
def get_tour(country: str, month: str):
    country = country.lower()
    month = month.lower()
    
    corrected_country = get_best_match(country, VALID_COUNTRIES)
    corrected_month = get_best_match(month, VALID_MONTHS)
    
    if not corrected_country:
        raise HTTPException(status_code=400, detail=f"Invalid country: '{country}'. Please enter a valid country.")
    if not corrected_month:
        raise HTTPException(status_code=400, detail=f"Invalid month: '{month}'. Please enter a valid month.")
    
    tour_info = TOUR_DATA.get(corrected_country, {}).get(corrected_month)
    if tour_info:
        return {"country": corrected_country.capitalize(), "month": corrected_month.capitalize(), "tour": tour_info}
    else:
        raise HTTPException(status_code=404, detail="No tour available for this selection.")

@app.post("/book-tour")
def book_tour(request: TourRequest):
    request_country = request.country.lower()
    request_month = request.month.lower()
    
    corrected_country = get_best_match(request_country, VALID_COUNTRIES)
    corrected_month = get_best_match(request_month, VALID_MONTHS)
    
    if not corrected_country:
        raise HTTPException(status_code=400, detail=f"Invalid country: '{request.country}'. Please enter a valid country.")
    if not corrected_month:
        raise HTTPException(status_code=400, detail=f"Invalid month: '{request.month}'. Please enter a valid month.")
    
    tour_info = TOUR_DATA.get(corrected_country, {}).get(corrected_month)
    if tour_info:
        return {"message": "Tour booked successfully!", "country": corrected_country.capitalize(), "month": corrected_month.capitalize(), "tour": tour_info}
    else:
        raise HTTPException(status_code=404, detail="No tour available for this selection.")
