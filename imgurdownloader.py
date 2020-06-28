import os
import sys
import urllib.request
import json
import requests

# urls = ['https://imgur.com/a/cGibB?grid', 'https://imgur.com/a/rBarn?grid']
urls = []
baseimgurl = 'https://imgur.com/ajaxalbums/getimages/'


def getname(url):
    '''Takes part of the url and use that as name'''
    name = url.split('/')[-1].split('?')[0]
    return (name)


def createdir(foldername):
    '''Create folder'''
    os.makedirs(foldername)


def getdata(url):
    '''Requests img data and build input for download'''

    imgurl = []

    name = getname(url)
    datainput = baseimgurl + name + '/hit.json'

    response = requests.get(datainput).content
    data = json.loads(response)
    data = (data['data']['images'])

    for d in data:
        imgurl.append(d['hash'] + d['ext'])
    try:
        createdir(name)
    except Exception:
        pass

    for i in imgurl:

        durl = 'https://i.imgur.com/' + i
        print('Downloading ' + durl)
        opner = urllib.request.build_opener()
        opner.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opner)
        urllib.request.urlretrieve(durl, os.path.join(name, i))


def main():
    '''Main function'''
    # print(str(sys.argv))

    for item in sys.argv[1:]:
        if 'imgur.com' in item:
            getdata(item)
        else:
            print('Not a imgur album')


#     for u in urls:
#         getdata(u)

if __name__ == "__main__":
    main()
