"""Input validation helpers."""


class ValidationError(ValueError):
    """Raised for invalid user input."""


def validate_city(city: str) -> str:
    city = city.strip()
    if not 2 <= len(city) <= 100:
        raise ValidationError("Enter a city name between 2 and 100 characters.")
    if not all(char.isalpha() or char in " .'-" for char in city):
        raise ValidationError("City names may contain letters, spaces, apostrophes, dots, and hyphens.")
    return city
