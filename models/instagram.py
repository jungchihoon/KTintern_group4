from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import shutil

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html)

imglist = []


for i in range(0, 60):

    insta = soup.select('.v1Nh3.kIKUG._bz0w')

    for i in insta:

        print('https://www.instagram.com'+ i.a['href'])
        imgUrl = i.select_one('.KL4Bh').img['src']
        imglist.append(imgUrl)
        imglist = list(set(imglist))
        html = driver.page_source
        soup = BeautifulSoup(html)
        insta = soup.select('.v1Nh3.kIKUG._bz0w')
        
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

n=0

for i in range(0, 60):
    # This is the image url.
    image_url = imglist[n]
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open('./img/' + plusUrl + str(n) + '.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    n +=1
    del resp

driver.close()
