import os
import json
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWEDAVIA_API_KEY")

BASE_URL = "https://api.swedavia.se/flightinfo/v2"

HEADERS = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Accept": "application/json"
}


def load_city_countries():
    with open(
        "city_country.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def get_departure_destinations():
    airport = "ARN"
    today = date.today().isoformat()

    url = f"{BASE_URL}/{airport}/departures/{today}"

    response = requests.get(url, headers=HEADERS)

    print("Status code:", response.status_code)

    data = response.json()
    flights = data["flights"]

    city_countries = load_city_countries()

    destinations = {}

    for flight in flights:
        status = flight.get("locationAndStatus", {}).get(
            "flightLegStatusEnglish",
            ""
        )

        if status == "Deleted":
            continue

        city = flight.get(
            "arrivalAirportEnglish",
            "Unknown"
        )

        destinations[city] = destinations.get(city, 0) + 1

    print("\nDestination overview")
    print("-" * 40)

    for city, count in sorted(destinations.items()):
        country = city_countries.get(city, "Unknown country")
        print(f"{city}, {country}: {count} flights")


if __name__ == "__main__":
    get_departure_destinations()