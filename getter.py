"""
Helper functions for getting a webpage and saving the image
"""
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
from io import BytesIO
from console import *
from fake_useragent import UserAgent
import json
import writer
import random
from time import sleep
TIMEOUT = 60 # 1 minute timeout
_ua = UserAgent(fallback="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0")

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








def _header():
    return {
        "User-Agent": _ua.random,
        "referer": "https://www.smackjeeves.com/",
    }


class GetterError(Exception):
    """
    Error for when the remote server gives you a valid 200 page but that doesn't have the content
    """
    def __init__(self, text: str):
        super(GetterError, self).__init__(text)


def Url(title: int, article: int)->str:
    return f"https://www.smackjeeves.com/discover/detail?titleNo={title}&articleNo={article}"

def saveImage(title: int, article: int) -> str:
    # short circuit for testing:
    # raise GetterError("Example Testing Error")
    # TODO -- this could be changed to the requests paramters file
    url = Url(title, article)

    req = requests.get(url, headers=_header(), timeout=TIMEOUT)
    req.raise_for_status()

    soup: BeautifulSoup = BeautifulSoup(req.text, features="html.parser")
    # specific to error handling
    if soup.title.string == "Error":
        raise RuntimeError("Error page raised")
    title = soup.find_all("h1", class_="header02__chapter-name")[0].string
    
    # currently -2 seems to get what I need
    script_source = soup.find_all("script")[-2].string
    # print(script_source) # debugging

    image_url: str = None
    re_pattern = r"\s*comicData:\s*\[\s*'(.*)'\s*,\s*]"
    
    if match := re.search(re_pattern, script_source):
        image_url = match.group(1)
    else: raise GetterError("Server raised psuedo-404 page")

    image_req = requests.get(image_url, _header(), timeout=TIMEOUT)
    image_req.raise_for_status()
    image_body = image_req.content # get binary data, as opposed to req.text

    with open(f"pages/comic-{article}.png", "wb+") as f:
        f.write(image_body)
        f.close()
    print(f"{INFO}Saved page #{article} -- \'{title}\'", 
            f"[comic-{article}.png]{END}"
    )
    # now for bonus information, we return the title
    return title

def fetchCover(url: str):
    """
    fet image data 
    """
    req = requests.get(url, _header(), timeout=60)
    req.raise_for_status()
    writer.atomicWrite(
        "cover.png",
        req.content,
        False
    )


def getList(url: str) -> list:
    """
    get the list of all of the metadata
    """
    req = requests.get(
        url,
        headers=_header(),
        timeout=TIMEOUT
    )
    body = req.json()
    # print(type(body))
    return body['result']['list']


if __name__ == "__main__":
    from pprint import pprint
    source = "https://www.smackjeeves.com/api/discover/articleList?titleNo=125360"
    data = getList(source)
    for x in range(5):
        pprint(data[x])
