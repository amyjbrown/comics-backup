"""
Backup Wildflowers
"""
# quick test to see if this loads properly
from time import sleep
import random
import requests

import metadata
from getter import saveImage, getList
from console import INFO, ALERT, DEBUG, END


delay_counter = 50
def randomDelay():
    global delay_counter

    def regular():
        """ 
        delay between [0,2) seconds
        """
        return random.random()

    def time():
        """
        get beta-variate time on [15,30] seconds
        """
        return random.betavariate(2, 3) * 15 + 14

    if delay_counter == 0:
        ammount = time()
        print(f"{DEBUG} * pre-emptive extra sleep for {ammount} seconds... {END}")
        sleep(ammount)
        delay_counter = random.randrange(40, 60)
    else:
        # random delay to keep things happy 
        sleep(regular())
    
    delay_counter -= 1

TITLE = 125360
# ARTICLE = 19
FINALPAGE = metadata.lastPage()
CURRENTPAGE = metadata.downloadedPages()

# this is where links to the articles, the pre-stub photos, and everything else can be downloaded 
LISTSOURCE = "https://www.smackjeeves.com/api/discover/articleList?titleNo=125360"

if CURRENTPAGE == FINALPAGE:
    print(f"{INFO}Finished Downloading!{END}")
    exit(0)
if CURRENTPAGE > FINALPAGE:
    print(f"{ALERT} !! Something went wrong, pages to download({CURRENTPAGE}) exceed max pages!{END}")
    exit(1)

# get list with metadata and begin recovering information from it
LIST = getList(LISTSOURCE)
metadata.recoverCover(LIST)

try: 
    for page in range(CURRENTPAGE+1, CURRENTPAGE + 301): # Account for smackjeeves page ranges [1..n] 
        tries = 0
        randomDelay()
        print(f"{INFO}Downloading page {page}...{END}")

        while True:

            try:
                page_title = saveImage(TITLE, page)
                # It'll display it's own success string here
                metadata.addPageData(
                    title=page_title,
                    file=f"wildflowers-{page}.png",
                    number=page,
                    timestamp=LIST[page-1]['distributedDate']
                )
                break


            except requests.exceptions.HTTPError as err:
                print(f"{ALERT} !! Error occured: {err}. Saving and exiting... {END}")
                metadata.backupData()
                exit(1)

            except RuntimeError as err:
                print(f"{DEBUG} * runtime error occured, presuming server timeout{END}")
                # attempt to wait between 3 and 10 minutes
                time = random.randrange(180, 600)
                print(f"{DEBUG} * iniating cooldown for {time // 60}:{time % 60}...{END}")
                sleep(time)
                print(f"{DEBUG} * cooldown finished, attempting to redownload {page}{END}")
                if tries < 5:
                    continue 
                else:
                    print(f"{ALERT} !! couldn't finish connection and download after 5 attempts, saving and exiting...")
                    metadata.backupData()
                    exit(1)
# Catch Control-C
except KeyboardInterrupt:
    metadata.backupData()
    print(f"{ALERT} !! Saving and exiting...{END}")
    exit(0)
# maange any other exception, unnescary but safe
except Exception as e:
    metadata.backupData()
    print(f"{ALERT} !! Caught {type(e)}:'{e}' caught, saving and exiting...{END}")
    exit(1)


# if the program exists successfuly, also save metadata
metadata.backupData()