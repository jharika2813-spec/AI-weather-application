# Weather AI App

A Flask weather dashboard that retrieves current conditions from OpenWeatherMap and uses Groq to generate practical weather advice.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `OPENWEATHER_API_KEY` and `GROQ_API_KEY` to `.env`.
4. Start the app: `flask --app app run --debug`

Open `http://127.0.0.1:5000` in a browser.

## Deploy on Render

The repository includes `render.yaml`, so it can be deployed as a Render Blueprint:

1. In Render, connect your GitHub account and select **New > Blueprint**.
2. Select this repository and its `main` branch. Render detects `render.yaml`.
3. Enter values for `OPENWEATHER_API_KEY` and `GROQ_API_KEY` when prompted, then deploy.

Render installs dependencies with `pip install -r requirements.txt` and starts the app with `gunicorn app:app`. Keep API keys in Render's environment-variable settings; never commit them to `.env`.
