from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

def color_tag(text):
    colors = {
        '[info]': Fore.BLUE + '[info]' + Style.RESET_ALL,
        '[WAR]': Fore.YELLOW + '[WAR]' + Style.RESET_ALL,
        '[ERROR]': Fore.RED + '[ERROR]' + Style.RESET_ALL,
        '[Finding]': Fore.GREEN + '[Finding]' + Style.RESET_ALL,
        '[logo]': Fore.CYAN + LOGO + Style.RESET_ALL,
    }
    return colors.get(text, text)

LOGO = r"""
▗▖  ▗▖▗▄▄▄▖ ▗▄▖ ▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖
▐▛▚▞▜▌▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌    ▝▚▞▘ ▐▌   
▐▌  ▐▌▐▛▀▀▘▐▌ ▐▌▐▌ ▐▌▐▛▀▀▘  ▐▌  ▐▛▀▀▘
▐▌  ▐▌▐▙▄▄▖▝▚▄▞▘▐▙█▟▌▐▙▄▄▖  ▐▌  ▐▙▄▄▖

        Coded By: Eslam Akl
     Blog: eslam3kl.gitbook.io
         Thanks to ChatGPT                      
"""

today_str = datetime.now().strftime("%d%m%Y")
OUTPUT_FILE = f"{today_str}-output.txt"
