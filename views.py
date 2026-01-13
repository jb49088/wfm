from utils import clear_screen

MENU_OPTIONS = [
    "Search for item",
    "Show my listings",
    "Sync my listings",
    "Change my status",
    "Profile",
    "Quit",
]


def menu():
    clear_screen()

    left = "wfm_cli"
    right = "In-Game"

    # Determine menu width
    menu_width = max(len(option) for option in MENU_OPTIONS + [left, right]) + 3

    # Align header
    spacing = menu_width - len(left) - len(right)
    print(f"{left}{' ' * spacing}{right}")
    print()

    # Menu options
    for i, option in enumerate(MENU_OPTIONS, 1):
        print(f"{i}. {option}")
    print()
