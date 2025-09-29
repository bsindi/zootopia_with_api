import os
import sys
import html
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.api-ninjas.com/v1/animals"

def fetch_animals(query: str):
    """Fetch animal data from API Ninjas Animals endpoint."""
    api_key = os.getenv("API_NINJAS_KEY")
    if not api_key:
        print("Error: Please set the environment variable API_NINJAS_KEY.")
        sys.exit(1)

    headers = {"X-Api-Key": api_key}
    resp = requests.get(API_URL, headers=headers, params={"name": query}, timeout=20)
    resp.raise_for_status()
    return resp.json()  # list of animals

def serialize_animal(animal_obj: dict) -> str:
    """Serializes an animal object (API Ninjas schema) into your card-style HTML."""
    name = html.escape(animal_obj.get("name", "Unknown"))

    characteristics = animal_obj.get("characteristics") or {}
    diet = html.escape(characteristics.get("diet", "Unknown"))
    animal_type = html.escape(characteristics.get("type", "Unknown"))

    locations = animal_obj.get("locations") or []
    location_display = html.escape(locations[0]) if locations else "Unknown"

    output = []
    output.append("<li class='cards__item'>")
    output.append(f"<div class='card__title'>{name}</div>")
    output.append("<div class='card__text'>")
    output.append("<ul>")
    output.append(f"<li><strong>Diet:</strong> {diet}</li>")
    output.append(f"<li><strong>Location:</strong> {location_display}</li>")
    output.append(f"<li><strong>Type: </strong>{animal_type}</li>")
    output.append("</ul>")
    output.append("</div>")
    output.append("</li>")
    return "\n".join(output)

def main():
    # Ask user for an animal name
    query = input("Enter the name of an animal: ").strip()
    if not query:
        print("Please enter a name.")
        sys.exit(0)

    # Fetch from API
    animals_data = fetch_animals(query)

    # Read template file
    with open("animals_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Build content
    items_html = "\n".join(serialize_animal(a) for a in animals_data)

    # Replace placeholder
    new_html = template.replace("__REPLACE_ANIMALS_INFO__", items_html)

    # Write new HTML file
    with open("animals.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("Website was successfully generated into the file animals.html.")

if __name__ == "__main__":
    main()
