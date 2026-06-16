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


def check_departures():
    print("Departures coming soon")


def search_flight():
    print("Search flight coming soon")


def run_odata_query():
    print("OData query coming soon")


def check_api_health():
    print("API health coming soon")


def run_auto_demo():
    print("Auto-demo coming soon")


def show_menu():
    print("\n=== Swedavia FlightInfo API v2 ===")
    print("1. View arrivals")
    print("2. View departures")
    print("3. Search specific flight")
    print("4. Run OData query")
    print("5. Check API health")
    print("6. Run full auto-demo")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose option: ")

        if choice == "1":
            check_arrivals()
        elif choice == "2":
            check_departures()
        elif choice == "3":
            search_flight()
        elif choice == "4":
            run_odata_query()
        elif choice == "5":
            check_api_health()
        elif choice == "6":
            run_auto_demo()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()