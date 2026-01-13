from utils import clear_screen, display_navbar

OPTIONS = [
    "Search for item",
    "Show my listings",
    "Sync my listings",
    "Change my status",
    "Authenticate",
    "Profile",
    "Log out",
    "Quit",
]

breadcrumbs = ["wfm_cli"]


def display_menu():
    for i, option in enumerate(OPTIONS, 1):
        print(f"{i}. {option}")
    print()


def menu():
    clear_screen()
    display_navbar(breadcrumbs)
    display_menu()
