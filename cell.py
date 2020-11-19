from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.Chrome("c:\\Users\\aclass\\Downloads\\chromedriver.exe")
driver.get("https://movie.naver.com/")
elem = driver.find_element_by_class_name("ipt_tx_srch")
elem.send_keys("어벤져스")
elem.send_keys(Keys.RETURN)

continue_link = driver.find_element_by_partial_link_text('어벤져스')
continue_link.click()


soup = BeautifulSoup(driver.page_source, 'html.parser')

# 영화 디테일 페이지
overview = soup.select(".con_tx")[0].text

poster = soup.find("div",class_="poster")
#img의 경로를 받아온다
poster = poster.find("img")["src"]

director = soup.select(
    "#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > ul > li:nth-child(1) > a.tx_people"
    )[0].text
main_actor = soup.select(
    "#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > ul > li:nth-child(2) > a.tx_people"
)[0].text

print(poster)