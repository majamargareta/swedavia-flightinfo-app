# Swedavia FlightInfo App

A Python-based terminal application that uses the Swedavia FlightInfo API v2 to display real-time flight information for Stockholm Arlanda Airport (ARN).

## Features

### Flight Information

- View upcoming arrivals
- View upcoming departures
- Search for a specific flight number
- Run custom OData queries
- Check API availability and status
- Run an automatic demonstration of the application

### Destination Analysis

- Show departure destinations
- Show arrival origins
- Filter destinations by country
- Search destinations by city
- Generate city-country mappings from official Swedavia destination statistics

## Technologies Used

- Python 3
- Requests
- python-dotenv
- OpenPyXL
- Swedavia FlightInfo API v2

## Installation

### Clone the repository

```bash
git clone https://github.com/majamargareta/swedavia-flightinfo-app.git
cd swedavia-flightinfo-app
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a .env file

```env
SWEDAVIA_API_KEY=your_api_key_here
```

## Running the Application

### Start the flight information tool

```bash
python airport.py
```

### Start the destination analysis tool

```bash
python destinations.py
```

### Generate city-country mappings

```bash
python generate_city_country.py
```

## Data Sources

- Swedavia FlightInfo API v2
- Swedavia Destination Statistics 2025