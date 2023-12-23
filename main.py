from menu import MainMenu
from command import operations
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        operations()
    else:
        main_menu = MainMenu()
        main_menu.show()
