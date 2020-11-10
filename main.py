"""
Backup Wildflowers
"""
# quick test to see if this loads properly
from time import sleep
import random
import traceback
import requests

import metadata
from getter import saveImage, getList, GetterError
from console import INFO, ALERT, DEBUG, END


delay_counter = 30
def randomDelay():
    global delay_counter

    def regular():
        """ 
        delay between [0,2) seconds
        """
        return random.random() * 2

    def time():
        """
        get beta-variate time on [30,60] seconds
        """
        return random.randrange(30, 61)

    if delay_counter == 0:
        ammount = time()
        print(f"{DEBUG} * pre-emptive extra sleep for {ammount} seconds... *{END}")
        sleep(ammount)
        delay_counter = random.randrange(20, 40)
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
    print(f"{ALERT} !! Something went wrong, pages to download({CURRENTPAGE}) exceed max pages !! {END}")
    exit(1)

# get list with metadata and begin recovering information from it
# if this errors out frankly things are already fucked
try:
    from socket import gaierror
    from urllib3.exceptions import MaxRetryError, NewConnectionError
    from requests.exceptions import ConnectionError
    print(f"{INFO}Attempting to download article list...")
    LIST = getList(LISTSOURCE)
    metadata.recoverCover(LIST)
    
except (gaierror, MaxRetryError, NewConnectionError, ConnectionError) as err:
    print(f"{ALERT} !! Unable to make connection to acquire article list, check internet connection. Saving and exiting... !! {END}")
    print(f"{DEBUG} * Exception caught: * \n{END}")
    print(f"{DEBUG} {type(err)} : {err} {END}")
    metadata.backupData()
    exit(1)

# finally would make this appear, so I'm calling it hear
print(f"{INFO}Successfully downloaded article list")

try: 
    for page in range(CURRENTPAGE+1, CURRENTPAGE + 301): # Account for smackjeeves page ranges [1..n] 
        tries = 4 # to account for off by one, as at tries=0 error checking will still run
        randomDelay()
        progress = (0 if CURRENTPAGE == 0 
            else int(page / FINALPAGE * 100)
        )
        print(f"{INFO}Attemping to downloada page #{page}/#{FINALPAGE} ({progress}%)...{END}")

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

            # this should catch both any requests.raiseforstatus(), connection/timeout errors
            # maybe should handle response errors uniquely?
            # e.g. timeout/connection errors
            except (requests.exceptions.RequestException, GetterError) as err:
                print(f"{DEBUG} * Runtime error occured, presuming server timeout * {END}")
                print(f"{DEBUG} * Exception info: {type(err)}:*{END}")
                print(f"{DEBUG}", err, "{END}")

                # attempt to wait between 1 and 3 minutes
                time = random.randrange(60, 180)
                print(f"{DEBUG} * iniating cooldown for {time // 60}:{time % 60}... * {END}")
                sleep(time)

                print(f"{INFO}Cooldown finished, attempting to redownload page #{page}(try {5 - tries + 1}/5){END}")
                if tries >= 0:
                    tries -= 1
                    continue 

                else:
                    print(f"{ALERT} !! couldn't make connection and download page #{page} after 5 attempts, saving and exiting... !! {END}")
                    metadata.backupData()
                    exit(1)

# Catch Control-C
except KeyboardInterrupt:
    metadata.backupData()
    print(f"{ALERT} !! Keybord Interupt. Saving and exiting... !! {END}")
    exit(0)
# reraises exception caused by calling exit() to work
except SystemExit as err:
    metadata.backupData() # just in case!
    raise 
except:
    metadata.backupData()
    print(f"{ALERT} !! Caught unexpected exception, saving and exiting... !! {END}")
    print(
        f"{DEBUG}* Stack Trace Info: * \n",
        traceback.format_exc(),
        f"{END}"
    )
    exit(1)

# I could maybe make this more organic with a _finally_ 
# if the program exists successfuly, also save metadata
metadata.backupData()