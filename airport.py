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
    airport = "ARN"
    today = date.today().isoformat()

    url = f"{BASE_URL}/{airport}/departures/{today}"
    response = requests.get(url, headers=HEADERS)

    print("Status code:", response.status_code)

    data = response.json()
    flights = data["flights"]

    print("Antal flyg:", data["numberOfFlights"])
    print()

    for flight in flights[:10]:
        flight_id = flight.get("flightId", "Okänt flyg")
        destination = flight.get("arrivalAirportEnglish", "Okänd destination")
        airline = flight.get("airlineOperator", {}).get("name", "Okänt flygbolag")
        status = flight.get("locationAndStatus", {}).get(
            "flightLegStatusEnglish",
            "Okänd status"
        )

        print(f"{flight_id}")
        print(f"Till: {destination}")
        print(f"Flygbolag: {airline}")
        print(f"Status: {status}")
        print("-" * 40)


def search_flight():
    airport = "ARN"
    today = date.today().isoformat()
    search_term = input("Enter flight number: ").upper()

    urls = [
        f"{BASE_URL}/{airport}/arrivals/{today}",
        f"{BASE_URL}/{airport}/departures/{today}"
    ]

    found = False

    for url in urls:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        for flight in data["flights"]:
            if flight.get("flightId", "").upper() == search_term:
                found = True

                print("\nFlight found:")
                print(f"Flight: {flight.get('flightId', 'Unknown')}")
                print(f"Airline: {flight.get('airlineOperator', {}).get('name', 'Unknown')}")
                print(f"Status: {flight.get('locationAndStatus', {}).get('flightLegStatusEnglish', 'Unknown')}")
                print(f"From: {flight.get('departureAirportEnglish', 'ARN')}")
                print(f"To: {flight.get('arrivalAirportEnglish', 'ARN')}")
                print("-" * 40)

    if not found:
        print("No flight found with that flight number.")


def run_odata_query():
    print("\nOData Query")
    print("Example:")
    print("airport eq 'ARN' and flightType eq 'D'")
    print()

    filter_query = input("Enter OData filter: ")
    count = input("How many results? Default 10: ")

    if count == "":
        count = 10
    else:
        count = int(count)

    url = f"{BASE_URL}/query"

    params = {
        "filter": filter_query,
        "count": count
    }

    response = requests.get(url, headers=HEADERS, params=params)

    print("Status code:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return

    data = response.json()
    flights = data.get("flights", [])

    print(f"Results: {len(flights)}")
    print()

    for item in flights:
        flight = item.get("departure") or item.get("arrival")

        if not flight:
            continue

        flight_id = flight.get("flightId", "Unknown")
        airline = flight.get("airlineOperator", {}).get("name", "Unknown")
        status = flight.get("locationAndStatus", {}).get(
            "flightLegStatusEnglish",
            "Unknown"
        )

        from_airport = flight.get("departureAirportEnglish", "ARN")
        to_airport = flight.get("arrivalAirportEnglish", "ARN")

        print(f"Flight: {flight_id}")
        print(f"Airline: {airline}")
        print(f"From: {from_airport}")
        print(f"To: {to_airport}")
        print(f"Status: {status}")
        print("-" * 40)


def check_api_health():
    airport = "ARN"
    today = date.today().isoformat()
    url = f"{BASE_URL}/{airport}/arrivals/{today}"

    response = requests.get(url, headers=HEADERS)

    print("\nAPI Health Check")
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("API is working.")
    elif response.status_code == 401:
        print("Unauthorized. Check your API key.")
    elif response.status_code == 404:
        print("Endpoint not found.")
    else:
        print("API returned an unexpected response.")


def run_auto_demo():
    print("\n=== AUTO DEMO START ===\n")

    print("1. Arrivals")
    check_arrivals()

    print("\n2. Departures")
    check_departures()

    print("\n=== AUTO DEMO END ===")


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