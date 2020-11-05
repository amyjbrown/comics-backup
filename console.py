__all__ = ['INFO', 'DEBUG', 'ALERT', 'END']
from colorama import Fore, Style, init
INFO = Fore.GREEN
DEBUG = Fore.YELLOW
ALERT = Fore.RED
END = Style.RESET_ALL

init()
