"""
Backup Wildflowers
"""
# quick test to see if this loads properly
from getter import saveImage
import random
from time import sleep
import requests

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
        print(f"pre-emptive extra sleep for {ammount} seconds...")
        sleep(ammount)
        delay_counter = 0
    else:
        sleep(random.randrange(0, 10))
    
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
            print(f"Error occured: {err}")
            exit(1)
        except RuntimeError as err:
            print("runtime error occured, presuming server timeout")
            # attempt to wait between 2 and 5 minutes
            time = random.randrange(120, 300)
            print(f"iniating cooldown for {time // 60}:{time % 60}...")
            sleep(time)
            print(f"cooldown finished, attempting to redownload {page}")
            if tries < 5:
                continue 
            else:
                exit(1)