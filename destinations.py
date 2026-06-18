import os
import json
import requests
from datetime import date
from dotenv import load_dotenv

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


def load_city_countries():
    """Load city-country mappings from the local JSON file."""
    with open("city_country.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_flights(airport, flight_type):
    """Fetch arrivals or departures from Swedavia API for today's date."""
    today = date.today().isoformat()
    url = f"{BASE_URL}/{airport}/{flight_type}/{today}"

    response = requests.get(url, headers=HEADERS)
    print("Status code:", response.status_code)

    data = response.json()
    return data["flights"]


def get_city_from_flight(flight, flight_type):
    """Return the relevant city depending on if the flight is an arrival or departure."""
    if flight_type == "departures":
        return flight.get("arrivalAirportEnglish", "Unknown")

    return flight.get("departureAirportEnglish", "Unknown")


def build_destination_overview(flight_type):
    """Build a dictionary with destinations, countries, and flight counts."""
    airport = "ARN"
    flights = get_flights(airport, flight_type)
    city_countries = load_city_countries()

    destinations = {}

    for flight in flights:
        status = flight.get("locationAndStatus", {}).get(
            "flightLegStatusEnglish",
            ""
        )

        # Skip deleted flights so the overview only shows active/relevant routes.
        if status == "Deleted":
            continue

        city = get_city_from_flight(flight, flight_type)
        country = city_countries.get(city, "Unknown country")

        # Create a new destination entry if the city has not been seen before.
        if city not in destinations:
            destinations[city] = {
                "country": country,
                "count": 0
            }

        # Count how many flights are connected to each city.
        destinations[city]["count"] += 1

    return destinations


def print_destination_overview(destinations):
    """Print all destinations with country and number of flights."""
    print("\nDestination overview")
    print("-" * 40)

    for city, info in sorted(destinations.items()):
        country = info["country"]
        count = info["count"]
        print(f"{city}, {country}: {count} flights")


def show_departure_destinations():
    """Show all departure destinations from Arlanda."""
    destinations = build_destination_overview("departures")
    print_destination_overview(destinations)


def show_arrival_origins():
    """Show all origin cities for arrivals to Arlanda."""
    destinations = build_destination_overview("arrivals")
    print_destination_overview(destinations)


def filter_by_country():
    """Filter destination overview by country."""
    flight_type = input("Choose flight type (Arrivals/Departures): ").lower()
    country_filter = input("Enter country name: ").lower()

    destinations = build_destination_overview(flight_type)

    print(f"\nResults for country: {country_filter.title()}")
    print("-" * 40)

    found = False

    for city, info in sorted(destinations.items()):
        country = info["country"]
        count = info["count"]

        if country.lower() == country_filter:
            found = True
            print(f"{city}, {country}: {count} flights")

    if not found:
        print("No destinations found for that country.")


def search_city():
    """Search for destinations or origins by city name."""
    flight_type = input("Choose flight type (Arrivals/Departures): ").lower()
    city_filter = input("Enter city name: ").lower()

    destinations = build_destination_overview(flight_type)

    print(f"\nSearch results for city: {city_filter}")
    print("-" * 40)

    found = False

    for city, info in sorted(destinations.items()):
        country = info["country"]
        count = info["count"]

        if city_filter in city.lower():
            found = True
            print(f"{city}, {country}: {count} flights")

    if not found:
        print("No city found.")


def show_menu():
    """Display the destinations menu."""
    print("\n=== Destinations Overview ===")
    print("1. Show departure destinations")
    print("2. Show arrival origins")
    print("3. Filter by country")
    print("4. Search city")
    print("0. Exit")


def main():
    """Main program loop for the destinations tool."""
    while True:
        show_menu()
        choice = input("Choose option: ")

        if choice == "1":
            show_departure_destinations()
        elif choice == "2":
            show_arrival_origins()
        elif choice == "3":
            filter_by_country()
        elif choice == "4":
            search_city()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


# Start the destinations tool only when this file is run directly.
if __name__ == "__main__":
    main()