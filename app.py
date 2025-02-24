from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

# Updated tour data with specific dates
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

@app.get("/tours")
def get_tours(
    full_name: str = Query(..., description="Your full name"),
    country: str = Query(..., description="Country you want to tour (Kenya, Tanzania, South Africa)"),
    month: str = Query(..., description="Month you want to travel (January, February, March)")
):
    country = country.title()
    month = month.title()

    if country not in TOUR_DATA:
        return {"error": "Invalid country. Choose from Kenya, Tanzania, or South Africa."}

    if month not in TOUR_DATA[country]:
        return {"error": "Invalid month. Choose from January, February, or March."}

    available_tours = TOUR_DATA[country][month]

    return {
        "full_name": full_name,
        "country": country,
        "month": month,
        "tours_available": available_tours
    }

class TourBooking(BaseModel):
    full_name: str
    passport_or_id: str
    country: str
    month: str
    tour_name: str
    number_of_people: int

@app.post("/book-tour")
def book_tour(booking: TourBooking):
    country = booking.country.title()
    month = booking.month.title()

    if country not in TOUR_DATA or month not in TOUR_DATA[country]:
        return {"error": "Invalid country or month. Choose from Kenya, Tanzania, or South Africa in January, February, or March."}

    selected_tour = next((tour for tour in TOUR_DATA[country][month] if tour["tour_name"] == booking.tour_name), None)

    if not selected_tour:
        return {"error": "Invalid tour name. Please choose from available tours."}

    total_cost = selected_tour["price_per_person"] * booking.number_of_people

    return {
        "message": "Tour booking successful!",
        "full_name": booking.full_name,
        "passport_or_id": booking.passport_or_id,
        "country": country,
        "month": month,
        "tour_name": booking.tour_name,
        "destination": selected_tour["destination"],
        "tour_dates": selected_tour["dates"],
        "number_of_people": booking.number_of_people,
        "price_per_person": selected_tour["price_per_person"],
        "total_cost": total_cost,
        "currency": "USD"
    }
