"""Flask entry point for the Weather AI application."""

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

from services.groq_service import GroqServiceError, get_weather_advice
from services.weather_service import WeatherServiceError, get_weather
from utils.helpers import ValidationError, validate_city

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        """Lightweight endpoint for Render health checks."""
        return jsonify({"status": "ok"})

    @app.get("/api/weather")
    def weather():
        try:
            city = validate_city(request.args.get("city", ""))
            return jsonify(get_weather(city))
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400
        except WeatherServiceError as error:
            return jsonify({"error": str(error)}), 502
        except Exception:
            app.logger.exception("Unexpected weather endpoint error")
            return jsonify({"error": "An unexpected server error occurred."}), 500

    @app.post("/api/advice")
    def advice():
        payload = request.get_json(silent=True) or {}
        weather = payload.get("weather")
        if not isinstance(weather, dict):
            return jsonify({"error": "A weather object is required."}), 400
        try:
            return jsonify({"advice": get_weather_advice(weather)})
        except GroqServiceError as error:
            return jsonify({"error": str(error)}), 502
        except Exception:
            app.logger.exception("Unexpected advice endpoint error")
            return jsonify({"error": "An unexpected server error occurred."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
