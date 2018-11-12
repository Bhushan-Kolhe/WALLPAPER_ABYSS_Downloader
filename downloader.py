import requests as r
from bs4 import BeautifulSoup
import shutil
import sys
import os
import argparse

def download_image(url):
    source = r.get(url).text
    soup = BeautifulSoup(source,'lxml')
    #print(soup.prettify())
    a = soup.find('img',class_='img-responsive')
    span = soup.find('span', class_='btn btn-success btn-custom download-button').attrs
    img = span['data-id'] + '.' + span['data-type']

    image = r.get(a.attrs['src'], stream=True)
    with open(folder + '/'+img, 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)
    del image
    del source


parser = argparse.ArgumentParser()
parser.add_argument("url", help="Enter WALLPAPER ABYSS/wall.alphacoders.com url")
parser.add_argument("--folder", help="To create a folder where you want to store images")
args = parser.parse_args()

count = 0
url = 'https://wall.alphacoders.com/'
#pageurl = 'https://wall.alphacoders.com/search.php?search=candice&page=1'
pageurl = args.url
#print(pageurl)
#print(args.folder)
if args.folder != None:
    folder = args.folder
else:
    folder = 'images'
#print(folder)
if not os.path.exists(folder):
        os.mkdir(folder)

while True:
    page = r.get(pageurl).text
    soup = BeautifulSoup(page, 'lxml')

    for i in soup.find_all('div', class_='thumb-container-big'):
        count += 1
        print(str(count) + ": " +url + i.a.attrs['href'])
        download_image(url + i.a.attrs['href'])
    
    pagination = soup.find('ul', class_='pagination pagination')
    next_ = pagination.find_all('li')[2]
    pageurl = url + next_.a.attrs['href']
    if pagination.find_all('li')[2].attrs == {'class': ['active']}:
        break
    del page

    #break
print(count)