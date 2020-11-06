"""
Backup Wildflowers
"""
# quick test to see if this loads properly
from time import sleep
import random
import requests

import metadata
from getter import saveImage
from console import INFO, ALERT, DEBUG, END


delay_counter = 0
def randomDelay():
    global delay_counter

    def regular():
        return random.random() * 5.5 + 0.5 

    def time():
        """
        get beta-variate time on [15,30] seconds
        """
        return random.betavariate(2, 3) * 15 + 14

    if delay_counter > 100:
        ammount = time()
        print(f"{DEBUG} * pre-emptive extra sleep for {ammount} seconds... {END}")
        sleep(ammount)
        delay_counter = 0
    else:
        # random delay to keep things happy 
        sleep(regular())
    
    delay_counter += random.randrange(6, 10)

TITLE = 125360
# ARTICLE = 19
FINALPAGE = metadata.lastPage()
CURRENTPAGE = metadata.downloadedPages()

# this is where links to the articles, the pre-stub photos, and everything else can be downloaded 
LISTDATA = "https://www.smackjeeves.com/api/discover/articleList?titleNo=125360"

if CURRENTPAGE == FINALPAGE:
    print(f"{INFO}Finished Downloading!{END}")
    exit(0)
if CURRENTPAGE > FINALPAGE:
    print(f"{ALERT} !! Something went wrong, pages to download({CURRENTPAGE}) exceed max pages!{END}")
    exit(1)

for page in range(CURRENTPAGE+1, FINALPAGE+1): # Account for smackjeves page ranges [1..n] 
    tries = 0
    randomDelay()
    print(f"{INFO}Downloading page {page}...{END}")
    while True:
        try:
            saveImage(TITLE, page)
            # It'll display it's own success image here
            break
        except requests.exceptions.HTTPError as err:
            print(f"{ALERT} !! Error occured: {err} {END}")
            exit(1)
        except RuntimeError as err:
            print(f"{ALERT} !! runtime error occured, presuming server timeout{END}")
            # attempt to wait between 3 and 10 minutes
            time = random.randrange(180, 600)
            print(f"{DEBUG} * iniating cooldown for {time // 60}:{time % 60}...{END}")
            sleep(time)
            print(f"{DEBUG} * cooldown finished, attempting to redownload {page}{END}")
            if tries < 5:
                continue 
            else:
                exit(1)