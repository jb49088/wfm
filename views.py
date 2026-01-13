from utils import clear_screen, display_navbar

MENU_OPTIONS = [
    "Search for item",
    "Show my listings",
    "Sync my listings",
    "Change my status",
    "Authenticate",
    "Profile",
    "Log out",
    "Quit",
]


def menu():
    clear_screen()
    display_navbar(["wfm_cli"])
    for i, option in enumerate(MENU_OPTIONS, 1):
        print(f"{i}. {option}")
    print()


def item_search():
    clear_screen()
    display_navbar(["wfm_cli", "Search for item"])
