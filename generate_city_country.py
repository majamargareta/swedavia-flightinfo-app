from openpyxl import load_workbook
import json

EXCEL_FILE = "destinations-statistik-2025.xlsx"

workbook = load_workbook(EXCEL_FILE)
sheet = workbook.active

city_country = {}

for row in sheet.iter_rows(min_row=9, values_only=True):
    country = row[0]
    city = row[1]

    if not country or not city:
        continue

    if "Summa" in str(country):
        continue

    city_country[city] = country.title()


manual_mappings = {
    "Arvidsjaur": "Sweden",
    "Gällivare": "Sweden",
    "Göteborg": "Sweden",
    "Hemavan Tärnaby": "Sweden",
    "Kalmar": "Sweden",
    "Karlstad": "Sweden",
    "Kiruna": "Sweden",
    "Luleå": "Sweden",
    "Malmö": "Sweden",
    "Ronneby": "Sweden",
    "Skellefteå": "Sweden",
    "Sundsvall": "Sweden",
    "Sveg": "Sweden",
    "Torsby": "Sweden",
    "Umeå": "Sweden",
    "Vilhelmina": "Sweden",
    "Visby": "Sweden",
    "Ängelholm": "Sweden",
    "Åre Östersund": "Sweden",

    "London LHR": "Great Britain",
    "London LGW": "Great Britain",
    "London STN": "Great Britain",
    "Paris CDG": "France",
    "Paris ORY": "France",
    "Rome FCO": "Italy",
    "Milan LIN": "Italy",
    "Milan MXP": "Italy",
    "New York JFK": "United States",
    "New York EWR": "United States",
    "Istanbul IST": "Turkey",
    "Istanbul SAW": "Turkey",
    "Warsaw WMI": "Poland",
    "Tokyo HND": "Japan",
    "Addis Abeba": "Ethiopia",
    "Alicante": "Spain",
    "Barcelona": "Spain",
    "Bergamo": "Italy",
    "Bergen": "Norway",
    "Bucharest OTP": "Romania",
    "Charleroi": "Belgium",
    "Cologne": "Germany",
    "Heraklion": "Greece",
    "Munich": "Germany",
    "Trapani": "Italy",
    "Tromso": "Norway",
    "Vaasa": "Finland",
    "Vilnius": "Lithuania"
}

city_country.update(manual_mappings)


with open(
    "city_country.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        city_country,
        file,
        ensure_ascii=False,
        indent=4
    )

print(f"Created city_country.json with {len(city_country)} cities")