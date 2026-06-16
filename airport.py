import os
import requests
from dotenv import load_dotenv
from datetime import date

load_dotenv()

API_KEY = os.getenv("SWEDAVIA_API_KEY")
BASE_URL = "https://api.swedavia.se/flightinfo/v2"

HEADERS = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Accept": "application/json"
}


def check_arrivals():
    airport = "ARN"
    today = date.today().isoformat()

    url = f"{BASE_URL}/{airport}/arrivals/{today}"
    response = requests.get(url, headers=HEADERS)

    print("Status code:", response.status_code)

    data = response.json()
    flights = data["flights"]

    print("Antal flyg:", data["numberOfFlights"])
    print()

    for flight in flights[:10]:
        flight_id = flight.get("flightId", "Okänt flyg")
        departure = flight.get("departureAirportEnglish", "Okänd stad")
        airline = flight.get("airlineOperator", {}).get("name", "Okänt flygbolag")
        status = flight.get("locationAndStatus", {}).get(
            "flightLegStatusEnglish",
            "Okänd status"
        )

        print(f"{flight_id}")
        print(f"Från: {departure}")
        print(f"Flygbolag: {airline}")
        print(f"Status: {status}")
        print("-" * 40)


if __name__ == "__main__":
    check_arrivals()