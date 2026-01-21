from typing import Any


def filter_listings(
    listings: list[dict[str, Any]], rank: int | None, status: str
) -> list[dict[str, Any]]:
    if rank is not None:
        listings = [listing for listing in listings if listing.get("rank") == rank]
    if status != "all":
        listings = [listing for listing in listings if listing.get("status") == status]

    return listings


def sort_listings(
    listings: list[dict[str, Any]],
    sort_by: str,
    order: str | None,
    default_orders: dict[str, str],
) -> tuple[list[dict[str, Any]], str]:
    if order is None:
        order = default_orders[sort_by]

    is_desc = order == "desc"

    sorted_listings = sorted(
        listings, key=lambda listing: listing["updated"], reverse=True
    )

    def get_sort_key(listing):
        if listing[sort_by] is None:
            return float("-inf") if is_desc else float("inf")

        if sort_by == "visibility":
            return "visible" if listing["visible"] else "hidden"

        return listing[sort_by]

    sorted_listings = sorted(
        sorted_listings,
        key=get_sort_key,
        reverse=is_desc,
    )

    return (sorted_listings, order)
