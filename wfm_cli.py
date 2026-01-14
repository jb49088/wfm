# ================================================================================
# =                                   WFM_CLI                                    =
# ================================================================================

from copy_user_listings import copy_user_listings
from display_item_listings import display_item_listings
from display_user_listings import display_user_listings


def wfm_cli():
    while True:
        try:
            cmd = input("wfm_cli> ").strip()
        except KeyboardInterrupt:
            break

        parts = cmd.split(maxsplit=1)

        if parts[0] == "search":
            display_item_listings(parts[1])


if __name__ == "__main__":
    try:
        wfm_cli()
    except KeyboardInterrupt:
        pass
