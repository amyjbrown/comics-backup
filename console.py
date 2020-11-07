__all__ = ['INFO', 'DEBUG', 'ALERT', 'END']
from colorama import Fore, Style, init
INFO = Fore.GREEN
DEBUG = Fore.YELLOW
ALERT = Fore.LIGHTRED_EX
END = Style.RESET_ALL

init()
