from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.co.kr/imghp?hl=ko")
elem = driver.find_element_by_name("q")
elem.send_keys("우럭회") #검색어 입력  # 검색어만 바꿔서 이미지 크롤링 하시면 되요~
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1
# 스크롤 높이 측정
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 페이지가 로딩 될대까지 대기
    time.sleep(SCROLL_PAUSE_TIME)
    # 스크롤 높이 계산 및 마지막 스크롤 높이와 비교
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 1
for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img').get_attribute("src")
        #opener=urllib.request.build_opener()
        #opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        #urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
        count = count + 1
    except:
        pass

driver.close()