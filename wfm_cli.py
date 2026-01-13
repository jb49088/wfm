# ================================================================================
# =                                   WFM_CLI                                    =
# ================================================================================

import sys

from copy_user_listings import copy_user_listings
from display_item_listings import display_item_listings
from display_user_listings import display_user_listings
from menu import menu
from utils import clear_screen, display_navbar, enter_alt_screen, exit_alt_screen


def wfm_cli():
    menu()
    option = input("> ")
    if option == "1":
        clear_screen()
        display_navbar(["wfm_cli", "Search for item"])
        item = input("> ")
        display_item_listings(item)
    elif option == "2":
        pass
    elif option == "7":
        exit_alt_screen()


if __name__ == "__main__":
    enter_alt_screen()
    try:
        wfm_cli()
    except KeyboardInterrupt:
        pass
    finally:
        exit_alt_screen()
