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

delay_counter = 0
def randomDelay():
    global delay_counter

    def time():
        """
        get beta-variate time on [1,10] seconds
        """
        return random.betavariate(2, 3) * 9 + 1

    if delay_counter > 100:
        ammount = time()
        print(f"{Fore.YELLOW}* pre-emptive extra sleep for {ammount} seconds... {END}")
        sleep(ammount)
        delay_counter = 0
    else:
        # random delay to keep things happy 
        sleep(random.randrange(0, 6))
    
    delay_counter += random.randrange(6, 13)

TITLE = 125360
# ARTICLE = 19

# saveImage(TITLE, ARTICLE)
# total articles = 2114
for page in range(1, 10):
    tries = 0
    randomDelay()
    print(f"Downloading page {page}...")
    while True:
        try:
            saveImage(TITLE, page)
            # It'll display it's own success image here
            break
        except requests.exceptions.HTTPError as err:
            print(f"{Fore.RED}! Error occured: {err} {END}")
            exit(1)
        except RuntimeError as err:
            print("{RED}! runtime error occured, presuming server timeout")
            # attempt to wait between 3 and 10 minutes
            time = random.randrange(180, 600)
            print(f"{Fore.YELLOW}* iniating cooldown for {time // 60}:{time % 60}...{END}")
            sleep(time)
            print(f"{Fore.YELLOW}* cooldown finished, attempting to redownload {page}{END}")
            if tries < 5:
                continue 
            else:
                exit(1)