import requests


def build_id_to_name_mapping() -> dict[str, str]:
    """Build id to name mapping dictionary."""
    r = requests.get("https://api.warframe.market/v2/items")
    r.raise_for_status()

    id_to_name = {item["id"]: item["i18n"]["en"]["name"] for item in r.json()["data"]}

    return id_to_name


def extract_user_listings(
    user: str, id_to_name: dict[str, str]
) -> dict[str, dict[str, int | bool | str]]:
    """Extract and process listings for a specific user."""
    r = requests.get(f"https://api.warframe.market/v2/orders/user/{user.lower()}")
    r.raise_for_status()

    listings = {}

    for listing in r.json()["data"]:
        if listing["type"] == "sell":
            listings[id_to_name[listing["itemId"]]] = {
                "price": listing["platinum"],
                "quantity": listing["quantity"],
                "visible": listing["visible"],
                "created": listing["createdAt"],
                "updated": listing["updatedAt"],
            }

    return listings
