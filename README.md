## weather-app

# Weather Monitoring System

This project monitors the weather conditions of major metro cities in India using the OpenWeather API. It collects and stores weather data in MongoDB, updates aggregate statistics such as maximum temperature every five minutes, and visualizes this data in a line graph using Dash.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Project](#running-the-project)
- [Usage](#usage)
  - [Weather Data Fetching](#weather-data-fetching)
  - [Data Processing and Alerts](#data-processing-and-alerts)
  - [Data Visualization](#data-visualization)

## Overview

This Weather Monitoring System continuously gathers weather data for key metro cities in India. The data is fetched every five minutes using the OpenWeather API and stored in a MongoDB database. Additionally, the system computes daily aggregate metrics such as minimum, maximum, and average temperatures. If the temperature in a city exceeds a specified threshold, an SMS alert is sent via Twilio. The system also includes a web-based dashboard using Dash and Plotly for data visualization, allowing users to view the weather data trends over time.

## Tech Stack

- **Python**: Core programming language.
- **OpenWeather API**: For fetching real-time weather data.
- **MongoDB**: For storing weather data and daily aggregates.
- **Dash & Plotly**: For data visualization in a web dashboard.
- **Twilio API**: For SMS alerts when temperature thresholds are exceeded.

## Features

1. **Real-Time Weather Monitoring**: Fetches weather data every 5 minutes for specified cities.
2. **Data Aggregation**: Calculates daily minimum, maximum, and average temperatures, as well as weather conditions for each city.
3. **SMS Notifications**: Sends an SMS alert if the temperature exceeds a predefined threshold using Twilio API.
4. **Data Visualization**: Displays daily weather aggregates in an interactive line graph using Dash.

## Project Structure

```
project/
├── run.py              # Main file to start the data fetching and processing
├── processor.py        # Handles weather data processing and threshold alerts
├── models.py           # Defines data models for weather data and summaries
├── data_store.py       # Manages MongoDB storage and retrieval of weather data
├── dashapp.py          # Dash application for data visualization
├── config.py           # Configuration file for the list of cities
└── README.md           # Project documentation
```

### File Descriptions

- **run.py**: The main script that initializes and runs the weather data monitoring process, fetching and storing data every five minutes.
- **processor.py**: Contains the `WeatherDataProcessor` class, responsible for fetching data, checking threshold alerts, and updating daily weather summaries.
- **models.py**: Defines the data models (`WeatherSummary`, `WeatherData`, and `WeatherAPIData`) using Pydantic for structured data representation.
- **data_store.py**: Contains the `WeatherDataStore` class, which handles interactions with the MongoDB database.
- **dashapp.py**: Dash application that serves a dashboard to visualize daily weather aggregates with interactive line graphs.
- **config.py**: Contains configuration data, including the list of cities being monitored.

## Environment Variables

The following environment variables need to be set:

- **wheather_api_key**: API key for OpenWeather.
- **mongo_host**: MongoDB connection URL.
- **twilio_api_sid**: Twilio API SID for sending SMS notifications.
- **twilio_api_token**: Twilio API token.
- **notification_number**: Phone number to send SMS alerts.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MongoDB (can be hosted or a local instance)
- Twilio account for SMS notifications

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/weather-monitoring-system.git
   cd weather-monitoring-system
2. Install required libraries:

  ```bash
pip install apscheduler pymongo twilio dash plotly requests pydantic pandas
```

3. Set up environment variables:

4. Configure environment variables for OpenWeather API, MongoDB, Twilio, and notification phone number.

### Running the Project

1. Start MongoDB if running locally.

2. Start the Data Fetcher: The run.py script fetches weather data and stores it in MongoDB every five minutes.
```bash
python run.py
```
3. Start the Dash Application: The dashapp.py script provides a web dashboard to view weather data.
```bash
python dashapp.py
```
4. Access the Dashboard: Open a web browser and navigate to http://127.0.0.1:8050.

## Usage

### Weather Data Fetching

- `run.py` initializes a scheduler (via APScheduler) to fetch data from the OpenWeather API every 5 minutes. Data is fetched for each city specified in `config.py` and processed to extract relevant information, including temperature, weather conditions, and timestamps.

### Data Processing and Alerts

- **Data Processing**: The `processor.py` script processes each data point, stores daily aggregates, and checks for temperature threshold breaches to trigger SMS alerts.
- **Data Aggregation**: The `WeatherDataProcessor` class in `processor.py` handles creating or updating daily weather summaries stored in MongoDB via `WeatherDataStore`.
- **SMS Alerts**: If the temperature exceeds a set threshold (defined in `run.py`), an SMS alert is sent to the configured phone number via Twilio.

### Data Visualization

- The `dashapp.py` file contains the Dash app, which displays daily weather aggregates for each city.
- **Interactive Dashboard**: The dashboard allows users to select a city from a dropdown and view a line graph showing daily maximum, minimum, and average temperatures over time.
- **Graphs**: The dashboard uses Plotly to generate line charts based on data from MongoDB, making it easy to visualize weather trends and patterns.


![alt text]([http://url/to/img.png](https://github.com/sarthaktayal174/weather-app/blob/main/weather_app/IMG8.png))
