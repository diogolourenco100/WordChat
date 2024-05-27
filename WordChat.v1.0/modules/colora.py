from colorama import init, Fore, Style

init()

def green(text):
    return Fore.GREEN + text + Style.RESET_ALL

def red(text):
    return Fore.RED + text + Style.RESET_ALL

def black(text):
    return Fore.BLACK + text + Style.RESET_ALL

def blue(text):
    return Fore.BLUE + text + Style.RESET_ALL

def yellow(text):
    return Fore.YELLOW + text + Style.RESET_ALL

def magenta(text):
    return Fore.MAGENTA + text + Style.RESET_ALL

def cyan(text):
    return Fore.CYAN + text + Style.RESET_ALL

def white(text):
    return Fore.WHITE + text + Style.RESET_ALL
