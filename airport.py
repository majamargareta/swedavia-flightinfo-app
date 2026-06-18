import os
import requests
from dotenv import load_dotenv
from datetime import date, datetime, timezone

# Load environment variables from the .env file.
load_dotenv()

# Read the Swedavia API key from the environment.
API_KEY = os.getenv("SWEDAVIA_API_KEY")

# Base URL for Swedavia FlightInfo API v2.
BASE_URL = "https://api.swedavia.se/flightinfo/v2"

# Headers required for all API requests.
HEADERS = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Accept": "application/json"
}


def get_relevant_flights(flights, time_key):
    """Filter out deleted flights and return upcoming flights sorted by time."""
    now = datetime.now(timezone.utc)
    active_flights = []

    for flight in flights:
        status = flight.get("locationAndStatus", {}).get(
            "flightLegStatusEnglish",
            ""
        )

        # Skip deleted flights so the user sees relevant flight information.
        if status == "Deleted":
            continue

        # Get the scheduled time from either arrivalTime or departureTime.
        scheduled_time = flight.get(time_key, {}).get("scheduledUtc")

        if not scheduled_time:
            continue

        # Convert the API time string into a Python datetime object.
        flight_time = datetime.fromisoformat(
            scheduled_time.replace("Z", "+00:00")
        )

        # Only keep flights that are still relevant from the current time.
        if flight_time >= now:
            active_flights.append(flight)

    # Sort flights by scheduled time, earliest first.
    active_flights.sort(
        key=lambda flight: flight.get(time_key, {}).get("scheduledUtc", "")
    )

    return active_flights


def check_arrivals():
    """Fetch and display upcoming arrivals for Arlanda Airport."""
    airport = "ARN"
    today = date.today().isoformat()

    # Build the arrivals endpoint URL.
    url = f"{BASE_URL}/{airport}/arrivals/{today}"
    response = requests.get(url, headers=HEADERS)

    print("Status code:", response.status_code)

    data = response.json()
    flights = data["flights"]

    print("Antal flyg:", data["numberOfFlights"])
    print()

    # Get the most relevant arrivals sorted by arrival time.
    relevant_flights = get_relevant_flights(flights, "arrivalTime")

    # Display the first 10 relevant arrivals.
    for flight in relevant_flights[:10]:
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
    """Fetch and display upcoming departures from Arlanda Airport."""
    airport = "ARN"
    today = date.today().isoformat()

    # Build the departures endpoint URL.
    url = f"{BASE_URL}/{airport}/departures/{today}"
    response = requests.get(url, headers=HEADERS)

    print("Status code:", response.status_code)

    data = response.json()
    flights = data["flights"]

    print("Antal flyg:", data["numberOfFlights"])
    print()

    # Get the most relevant departures sorted by departure time.
    relevant_flights = get_relevant_flights(flights, "departureTime")

    # Display the first 10 relevant departures.
    for flight in relevant_flights[:10]:
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
    """Search for a specific flight number in today's arrivals and departures."""
    airport = "ARN"
    today = date.today().isoformat()
    search_term = input("Enter flight number: ").upper()

    # Search both arrivals and departures for the selected airport and date.
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
    """Let the user run a custom OData query against the FlightInfo query endpoint."""
    print("\nOData Query")
    print("Example:")
    print("airport eq 'ARN' and flightType eq 'D'")
    print()

    filter_query = input("Enter OData filter: ")
    count = input("How many results? Default 10: ")

    # Use 10 results as default if the user leaves the field empty.
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

    # The query endpoint can return either arrival or departure objects.
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
    """Check if the API connection is working by making a real arrivals request."""
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
    """Run a short demo of the main flight functions."""
    print("\n=== AUTO DEMO START ===\n")

    print("1. Arrivals")
    check_arrivals()

    print("\n2. Departures")
    check_departures()

    print("\n=== AUTO DEMO END ===")


def show_menu():
    """Display the main CLI menu."""
    print("\n=== Swedavia FlightInfo API v2 ===")
    print("1. View arrivals")
    print("2. View departures")
    print("3. Search specific flight")
    print("4. Run OData query")
    print("5. Check API health")
    print("6. Run full auto-demo")
    print("0. Exit")


def main():
    """Main program loop for the terminal application."""
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


# Start the application only when this file is run directly.
if __name__ == "__main__":
    main()