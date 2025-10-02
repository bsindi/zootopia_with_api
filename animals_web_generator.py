# animals_web_generator.py
import sys
import html
import data_fetcher

def serialize_animal(animal_obj: dict) -> str:
    """Serialize an animal (API Ninjas schema) into your card-style HTML."""
    name = html.escape(animal_obj.get("name", "Unknown"))

    characteristics = animal_obj.get("characteristics") or {}
    diet = html.escape(characteristics.get("diet", "Unknown"))
    animal_type = html.escape(characteristics.get("type", "Unknown"))

    locations = animal_obj.get("locations") or []
    location_display = html.escape(locations[0]) if locations else "Unknown"

    parts = []
    parts.append("<li class='cards__item'>")
    parts.append(f"<div class='card__title'>{name}</div>")
    parts.append("<div class='card__text'>")
    parts.append("<ul>")
    parts.append(f"<li><strong>Diet:</strong> {diet}</li>")
    parts.append(f"<li><strong>Location:</strong> {location_display}</li>")
    parts.append(f"<li><strong>Type: </strong>{animal_type}</li>")
    parts.append("</ul>")
    parts.append("</div>")
    parts.append("</li>")
    return "\n".join(parts)

def build_error_card(query: str) -> str:
    """Nice message when no animal is found (Milestone 3)."""
    q = html.escape(query)
    return (
        "<li class='cards__item'>"
        "<div class='card__title'>No Results</div>"
        f"<div class='card__text'><h2>The animal \"{q}\" doesn't exist.</h2></div>"
        "</li>"
    )

def main():
    animal_name = input("Please enter an animal: ").strip()
    if not animal_name:
        print("Please enter a name.")
        sys.exit(0)

    # Get data from the separate fetcher module
    animals = data_fetcher.fetch_data(animal_name)

    # Read template
    with open("animals_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Build cards (or show a friendly message if none found)
    if animals:
        items_html = "\n".join(serialize_animal(a) for a in animals)
    else:
        items_html = build_error_card(animal_name)

    # Replace placeholder and write output
    new_html = template.replace("__REPLACE_ANIMALS_INFO__", items_html)
    with open("animals.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("Website was successfully generated into the file animals.html.")

if __name__ == "__main__":
    main()
