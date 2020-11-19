from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.Chrome("C:\\Users\\khjeo\\Downloads\\chromedriver_win32\\chromedriver.exe")
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
poster = poster.find("img")["src"]
poster = poster.split('?')
new_size = '?type=m203_290_2'
poster = poster[0] + new_size

# 3. staff & staff_image
people = soup.find_all("a", class_="thumb_people")
# 영화 감독 + 주연배우 5명 순서대로 list에 담겨져 있음
tx_people = []
thumb_people = []
for i in people:
    thumb_people.append(i.find("img")["src"])
    tx_people.append(i.find("img")["alt"])


netizen_score = soup.select(
    "#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.netizen_score > div > div > em"
)[0].text
special_score = soup.select(
    "#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.special_score > div > div > em"
)[0].text


running_time = soup.select(
    "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)"
)[0].text

genre = soup.select(
    "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a:nth-child(1)"
)[0].text

grade = soup.select(
    "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a"
)[0].text


download_url = soup.find("a",class_="btn_dnld")["href"]

count = soup.find("p", class_="count")[0].text

best_line1_character = soup.select(
    '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(1) > div > em > span'
)[0].text
best_line1 = soup.select(
    '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(1) > div > div > strong'
)[0].text

best_line2_character = soup.select(
    '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(2) > div > em > span'
)[0].text
best_line2 = soup.select(
    '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(2) > div > div > strong'
)[0].text

relate_movie = soup.find("ul", class_="thumb_link_mv").find_all("li")
# 5개가 default
relate_movies = []
relate_movies_thumb = []

for i in relate_movie:
    relate_movies.append(i.find("img")["alt"])
    relate_movies_thumb.append(i.find("img")["src"].strip(' \t\n\r'))

# 잘 알려진 keyword list 형태로 구현
aka_info = soup.find("div", class_="aka_info").find("p").text.split('|')
for i in range(len(aka_info)):
    aka_info[i] = aka_info[i].strip(' \x06\t\n\r')