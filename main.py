"""
Backup Wildflowers
"""
# quick test to see if this loads properly
from time import sleep
import random
import requests
from colorama import init, Fore, Back, Style
from getter import saveImage
END = Style.RESET_ALL

init()


delay_counter = 0
def randomDelay():
    global delay_counter

    def regular():
        return random.random() * 5.5 + 0.5 

    def time():
        """
        get beta-variate time on [10,20] seconds
        """
        return random.betavariate(2, 3) * 9 + 11

    if delay_counter > 100:
        ammount = time()
        print(f"{Fore.YELLOW}* pre-emptive extra sleep for {ammount} seconds... {END}")
        sleep(ammount)
        delay_counter = 0
    else:
        # random delay to keep things happy 
        sleep(regular())
    
    delay_counter += random.randrange(6, 10)

TITLE = 125360
# ARTICLE = 19

# saveImage(TITLE, ARTICLE)
# total articles = 2114
for page in range(1, 10):
    tries = 0
    randomDelay()
    print(f"{Fore.GREEN}Downloading page {page}...{END}")
    while True:
        try:
            saveImage(TITLE, page)
            # It'll display it's own success image here
            break
        except requests.exceptions.HTTPError as err:
            print(f"{Fore.RED}! Error occured: {err} {END}")
            exit(1)
        except RuntimeError as err:
            print("{RED}! runtime error occured, presuming server timeout{END}")
            # attempt to wait between 3 and 10 minutes
            time = random.randrange(180, 600)
            print(f"{Fore.YELLOW}* iniating cooldown for {time // 60}:{time % 60}...{END}")
            sleep(time)
            print(f"{Fore.YELLOW}* cooldown finished, attempting to redownload {page}{END}")
            if tries < 5:
                continue 
            else:
                exit(1)