"""
Helper functions for getting a webpage and saving the image
"""
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
from io import BytesIO
from colorama import Fore, Style
END = Style.RESET_ALL

# todo maybe obfuscate this more
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
}

def Url(title: int, article: int)->str:
    return f"https://www.smackjeeves.com/discover/detail?titleNo={title}&articleNo={article}"

def saveImage(title: int, article: int):

    # TODO -- this could be changed to the requests paramters file
    url = Url(title, article)

    req = requests.get(url, headers=headers)
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
    else: raise RuntimeError("Couldn't locate image url in script")

    image_req = requests.get(image_url, headers)
    image_req.raise_for_status()
    image_body = image_req.content # get binary data, as opposed to req.text

    with open(f"pages/wildflowers-{article}.png", "wb+") as f:
        f.write(image_body)
        f.close()
    print(f"{Fore.GREEN}Saved file #{article} -- {title}:", 
            f"wildflowers-{article}.png{END}"
    )

