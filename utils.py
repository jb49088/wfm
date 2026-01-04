import requests


def build_id_to_name_mapping() -> dict[str, str]:
    """Build id to name mapping dictionary."""
    r = requests.get("https://api.warframe.market/v2/items")
    r.raise_for_status()

    id_to_name = {}

    id_to_name = {item["id"]: item["i18n"]["en"]["name"] for item in r.json()["data"]}

    return id_to_name


def gather_user_listings(user: str) -> list[str]:
    """Gather listings for a specific user."""
    r = requests.get(f"https://api.warframe.market/v2/orders/user/{user.lower()}")
    r.raise_for_status()

    listings = [item["itemId"] for item in r.json()["data"]]

    return listings


def convert_ids_to_item_names(
    id_to_name: dict[str, str],
    listings: list[str],
) -> list[str]:
    """Convert listing IDs to in-game item names, alphabetically sorted."""
    items = [id_to_name[listing] for listing in listings]

    return sorted(items)
