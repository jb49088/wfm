from typing import Any

import aiohttp
import pyperclip
from prompt_toolkit import PromptSession

from api import extract_item_listings, extract_seller_listings, extract_user_listings
from display import (
    DEFAULT_ORDERS,
    RIGHT_ALLIGNED_COLUMNS,
    build_listings_rows,
    build_search_rows,
    build_seller_rows,
    determine_widths,
    display_listings,
)
from filters import filter_listings, sort_listings

# ===================================== COPY =====================================


def copy(listing_to_copy: dict[str, Any], max_ranks: dict[str, int | None]) -> None:
    """Copy a listing for in-game whispering."""
    item_name = listing_to_copy["item"]

    if listing_to_copy.get("rank") is not None:
        item_name = (
            f"{item_name} (rank {listing_to_copy['rank']}/{max_ranks[item_name]})"
        )

    segments = [
        "WTB",
        item_name,
        f"{listing_to_copy['price']}p",
    ]
    message = f"/w {listing_to_copy['seller']} {' | '.join(segments)}"

    pyperclip.copy(message)

    print(f"\nCopied to clipboard: {message}\n")


# ==================================== SEARCH ====================================


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
    data_rows = build_search_rows(sorted_item_listings, max_ranks)
    column_widths = determine_widths(data_rows, sort)
    display_listings(data_rows, column_widths, RIGHT_ALLIGNED_COLUMNS, sort, sort_order)

    return sorted_item_listings


# =================================== LISTINGS ===================================


async def listings(
    id_to_name: dict[str, str],
    max_ranks: dict[str, int | None],
    user: str,
    headers: dict[str, str],
    session: aiohttp.ClientSession,
    rank: int | None = None,
    sort: str = "updated",
    order: str | None = None,
) -> list[dict[str, Any]]:
    """Main entry point."""
    user_listings = await extract_user_listings(session, user, id_to_name, headers)
    filtered_item_listings = filter_listings(user_listings, rank, status="all")
    sorted_user_listings, sort_order = sort_listings(
        filtered_item_listings, sort, order, DEFAULT_ORDERS
    )
    data_rows = build_listings_rows(sorted_user_listings, max_ranks)
    column_widths = determine_widths(data_rows, sort)
    display_listings(data_rows, column_widths, RIGHT_ALLIGNED_COLUMNS, sort, sort_order)

    return sorted_user_listings


# ==================================== SELLER ====================================


async def seller(
    id_to_name: dict[str, str],
    max_ranks: dict[str, int | None],
    slug: str,
    seller: str,
    session: aiohttp.ClientSession,
    rank: int | None = None,
    sort: str = "updated",
    order: str | None = None,
) -> list[dict[str, Any]]:
    """Main entry point."""
    seller_listings = await extract_seller_listings(session, slug, seller, id_to_name)
    filtered_seller_listings = filter_listings(seller_listings, rank, status="all")
    sorted_seller_listings, sort_order = sort_listings(
        filtered_seller_listings, sort, order, DEFAULT_ORDERS
    )
    data_rows = build_seller_rows(sorted_seller_listings, max_ranks)
    column_widths = determine_widths(data_rows, sort)
    display_listings(data_rows, column_widths, RIGHT_ALLIGNED_COLUMNS, sort, sort_order)

    return sorted_seller_listings


# ==================================== LINKS =====================================


def _get_base_name(item_name: str) -> str:
    """Extract base name without part suffixes."""
    part_words = [
        "Set",
        "Blueprint",
        "Barrel",
        "Receiver",
        "Stock",
        "Neuroptics",
        "Chassis",
        "Systems",
        "Link",
        "Wings",
        "Pouch",
        "Stars",
        "Harness",
        "Grip",
        "Blade",
        "Lower Limb",
        "Handle",
        "Upper Limb",
        "String",
    ]
    words = item_name.split()
    # Remove known part words from the end
    while words and words[-1] in part_words:
        words.pop()

    return " ".join(words)


def _expand_item_sets(
    user_listings: list[dict[str, Any]], all_items: list[dict[str, Any]]
) -> list[str]:
    """Expand set items into individual parts for the set."""
    expanded_listings = []

    for listing in user_listings:
        if listing["item"].endswith(" Set"):
            set_base = _get_base_name(listing["item"])
            for item in all_items:
                item_name = item["i18n"]["en"]["name"]
                item_base = _get_base_name(item_name)
                if set_base == item_base and item_name != listing["item"]:
                    expanded_listings.append(item_name)
        else:
            expanded_listings.append(listing["item"])

    return expanded_listings


def _convert_listings_to_links(listings: list[str]) -> list[str]:
    """Process and format item names for ingame pasting."""
    return [
        f"[{listing.replace(' Blueprint', '')}]"
        if "Blueprint" in listing
        else f"[{listing}]"
        for listing in listings
    ]


def _chunk_links(links: list[str]) -> list[str]:
    """Break item list into 300 character chunks."""
    chunks = []
    current_chunk = []
    current_length = 0

    for link in links:
        link_length = len(link) + 1  # +1 for the space
        if current_length + link_length > 300:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(link)
        current_length += link_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


async def _copy_to_clipboard(chunks: list[str], prompt_session: PromptSession) -> None:
    for i, chunk in enumerate(chunks, 1):
        pyperclip.copy(chunk)
        if i < len(chunks):
            await prompt_session.prompt_async(
                f"\nChunk {i}/{len(chunks)} copied ({len(chunk)} chars). Press Enter for next chunk..."
            )
        else:
            print(f"\nChunk {i}/{len(chunks)} copied ({len(chunk)} chars).\n")


async def links(
    all_items: list[dict[str, Any]],
    id_to_name: dict[str, str],
    user: str,
    headers: dict[str, str],
    session: aiohttp.ClientSession,
    prompt_session: PromptSession,
    sort: str = "item",
    order: str | None = None,
) -> None:
    """Main entry point."""
    user_listings = await extract_user_listings(session, user, id_to_name, headers)
    sorted_user_listings, _ = sort_listings(user_listings, sort, order, DEFAULT_ORDERS)
    expanded_listings = _expand_item_sets(sorted_user_listings, all_items)
    links = _convert_listings_to_links(expanded_listings)
    link_chunks = _chunk_links(links)
    await _copy_to_clipboard(link_chunks, prompt_session)
