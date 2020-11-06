"""
Generates a metadata.json file that will act as an index for it
done because comic titles may not be able to be stored inside filenames

the file will look like
{
    "comic-title": "foo",                   // title of entire comic
    "author": "dave",                       // author of comic 
    "total-pages": 42,                      // total pages the file will contain, on [1, "total-pages"]
    "collected-pages": 2,                   // how many pages have been collected, starting from 1
                                            // 0 indicates no pages have been downlaoded
    "cover-page": "cover.png",              // cover page of comic -- either string or null
    "pages": [                              // list of data for each comic
        {
            "title": "intro",               // title of individual page
            "number:" 1,                    // current page number, for the sake of convnience
            "timestamp: "2007-04-05T14:30", // timestamp of comic posted
            "file": "foo-1.png"             // path to file for it
        },
        {                                   // etc.
            "title": "denounment",
            "number:" 2,
            "timestamp: "2007-04-012T02:45",
            "file": "foo-2.png"
        }
    ]
}
"""
# load json_stub
import json
import os
import datetime
import shutil
from pprint import pprint
import writer
import getter

# generate metadata.json from stub.json if it doesn't already exists, and store content in _file
_file = None
try:
    with open("metadata.json", "r") as f:
        _file = f.read()

except FileNotFoundError:
    with open("stub.json", "r") as f:
        contents = f.read()
        writer.atomicWrite("metadata.json", contents)
        _file = contents

_json_data = json.loads(_file)

def addPageData(title:str, file:str, number:int, timestamp: str):
    """
    updates information from new page
    each of the params fits exactly with the generated data file
    """
    # todo, generate and convert datetime
    section = {
        "title": title,
        "number": number,
        "timestamp": timestamp,
        "file": file,
    }

    # this is tricky, and maybe unatomic
    _json_data["pages"].append(section)
    # ensure we don't write out of sequeunce !!!
    if _json_data["collected-pages"] + 1 != number:
        current = _json_data["collected-pages"]
        raise ValueError(
            f"attempted to write metadata for page #{number}: \"{title}\" "
            f"but only {current} pages have been written, which means {number-current-1} pages have been missed!"
        )
    else: 
        _json_data["collected-pages"] += 1
    
    writer.atomicWrite(
        "metadata.json", 
        json.dumps(_json_data)
        )

def downloadedPages() -> int:
    """
    see number of pages which have been downloaded
    e.g. if foo-1, foo-2 and foo-3 have been downloaded, then return 3
    """
    return _json_data["collected-pages"]


def lastPage() -> int:
    """
    get the last page to be downloaded
    if a comic is 100 pages long, then lastPage() = 100
    """
    return _json_data["total-pages"]


def saveCover(data: list):
    """
    fetches and stores the cover page if it is not defined
    """
    if _json_data['cover-page'] is not None: return

    imgUrl = data['imgUrl']
    image = getter.fetchCover(imgUrl)
    writer.atomicWrite(
        file = "pages/cover.png",
        data = image,
        text = False
    )
    _json_data['cover-page'] = "cover.png" 
    

if __name__ == "__main__":
    source = "https://www.smackjeeves.com/api/discover/articleList?titleNo=125360"
    data = getter.getList(source)
    print(data)
    saveCover(data)