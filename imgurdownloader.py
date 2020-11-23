import json
import os
import pathlib
import sys
import urllib.request

import requests

BASEIMGURL = "https://imgur.com/ajaxalbums/getimages/"


def getname(url):
    """Take part of the url and use that as name."""
    return pathlib.PosixPath(url).stem


def createdir(directory):
    """Create folder."""
    os.makedirs(directory)


def getdata(url):
    """Request img data and build input for download."""
    imgurl = []

    albumname = getname(url)
    datainput = BASEIMGURL + albumname + "/hit.json"

    data = json.loads(requests.get(datainput).content)
    data = data["data"]["images"]

    for d in data:
        imgurl.append(d["hash"] + d["ext"])
    try:
        createdir(albumname)
    except Exception as Error:
        print(Error)

    imgurl = set(imgurl)
    print("{} img to be downloaded".format(len(imgurl)))
    for i, item in enumerate(imgurl):

        durl = "https://i.imgur.com/" + item
        print("Downloading [{}/{}] {}".format(i + 1, len(imgurl), durl))
        opner = urllib.request.build_opener()
        opner.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opner)
        urllib.request.urlretrieve(durl, os.path.join(albumname, item))


def main():
    """Verify input."""
    for item in sys.argv[1:]:
        if "imgur.com" in item:
            getdata(item)
        else:
            print("Not a imgur album")


if __name__ == "__main__":
    main()
