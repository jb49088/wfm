import pyperclip

from utils import (
    build_id_to_name_mapping,
    extract_user_listings,
)


def convert_listings_to_links(
    listings: dict[str, dict[str, int | bool | str]],
) -> list[str]:
    """Sort and format item names with surrounding brackets."""
    links = ["[" + listing + "]" for listing in listings]

    return sorted(links)


def chunk_links(links: list[str]) -> list[str]:
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


def copy_to_clipboard(chunks: list[str]) -> None:
    """Copy items to clipboard."""
    for i, chunk in enumerate(chunks, 1):
        pyperclip.copy(chunk)
        if i < len(chunks):
            input(
                f"Chunk {i}/{len(chunks)} copied ({len(chunk)} chars). Press Enter for next chunk..."
            )
        else:
            print(f"Chunk {i}/{len(chunks)} copied ({len(chunk)} chars).")


def copy_listings() -> None:
    """Main entry point."""
    id_to_name = build_id_to_name_mapping()
    listings = extract_user_listings("bhwsg", id_to_name)
    links = convert_listings_to_links(listings)
    chunks = chunk_links(links)
    copy_to_clipboard(chunks)


if __name__ == "__main__":
    copy_listings()
