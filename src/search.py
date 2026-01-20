from typing import Any

import aiohttp

from config import USER_AGENT
from utils import (
    determine_widths,
    display_listings,
    filter_listings,
    sort_listings,
)

DEFAULT_ORDERS = {
    "seller": "asc",
    "reputation": "desc",
    "status": "asc",
    "item": "asc",
    "price": "asc",
    "rank": "desc",
    "quantity": "desc",
    "created": "desc",
    "updated": "desc",
}
STATUS_MAPPING = {"offline": "Offline", "online": "Online", "ingame": "In Game"}
RIGHT_ALLIGNED_COLUMNS = ("price", "quantity", "reputation")


def slugify_item_name(item: str) -> str:
    """Convert item name to URL-safe slug."""
    return item.lower().replace(" ", "_")


async def extract_item_listings(
    session: aiohttp.ClientSession, item: str, id_to_name: dict[str, str]
) -> list[dict[str, Any]]:
    """Extract and process listings for a specific item."""
    async with session.get(
        url=f"https://api.warframe.market/v2/orders/item/{item}",
        headers=USER_AGENT,
    ) as r:
        r.raise_for_status()
        response_data = await r.json()

    item_listings = []
    for listing in response_data["data"]:
        if listing["type"] == "sell":
            item_listings.append(
                {
                    "seller": listing.get("user", {}).get("ingameName", "Unknown"),
                    "slug": listing.get("user", {}).get("slug", "Unknown"),
                    "reputation": listing.get("user", {}).get("reputation", 0),
                    "status": listing.get("user", {}).get("status", "offline"),
                    "item": id_to_name[listing.get("itemId", "")],
                    "itemId": listing.get("itemId", ""),
                    "rank": listing.get("rank"),
                    "price": listing.get("platinum", 0),
                    "quantity": listing.get("quantity", 1),
                    "updated": listing.get("updatedAt", ""),
                }
            )

    return item_listings


def build_rows(
    listings: list[dict[str, Any]], max_ranks: dict[str, int | None]
) -> list[dict[str, str]]:
    """Build rows for table rendering."""
    data_rows = []
    for i, listing in enumerate(listings, start=1):
        row = {
            "#": str(i),
            "seller": listing["seller"],
            "reputation": str(listing["reputation"]),
            "status": STATUS_MAPPING[listing["status"]],
            "item": listing["item"],
            "price": f"{listing['price']}p",
            "quantity": str(listing["quantity"]),
            "updated": str(listing["updated"]),
        }

        if listing.get("rank") is not None:
            row["rank"] = f"{listing['rank']}/{max_ranks[listing['item']]}"

        data_rows.append(row)

    return data_rows


async def search(
    item_slug: str,
    id_to_name: dict[str, str],
    max_ranks: dict[str, int | None],
    session: aiohttp.ClientSession,
    rank: int | None = None,
    sort: str = "price",
    order: str | None = None,
    status: str = "ingame",
) -> list[dict[str, Any]]:
    """Main entry point."""
    item_listings = await extract_item_listings(session, item_slug, id_to_name)
    filtered_item_listings = filter_listings(item_listings, rank, status)
    sorted_item_listings, sort_order = sort_listings(
        filtered_item_listings, sort, order, DEFAULT_ORDERS
    )
    data_rows = build_rows(sorted_item_listings, max_ranks)
    column_widths = determine_widths(data_rows, sort)
    display_listings(data_rows, column_widths, RIGHT_ALLIGNED_COLUMNS, sort, sort_order)

    return sorted_item_listings
