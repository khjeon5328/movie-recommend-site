from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint

driver = webdriver.Chrome("C:\\Users\\grey\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get("https://movie.naver.com/")
elem = driver.find_element_by_class_name("ipt_tx_srch")
elem.send_keys("어벤져스: 인피니티 워")
elem.send_keys(Keys.RETURN)

continue_link = driver.find_element_by_partial_link_text('어벤져스: 인피니티 워')
continue_link.click()


soup = BeautifulSoup(driver.page_source, 'html.parser')

# 영화 디테일 페이지
'''
overview
poster
staff
thumb_staff
netizen_score
special_score
running_time
genre
grade
download_url
count --> 없는 경우도 존재
best_line1_character
best_line1
best_line2_character
best_line2
relate_movies
relate_movies_thumb 
aka_info
viewer_img
'''



overview = soup.select(".con_tx")[0].text.replace('\xa0', '')

poster = soup.find("div",class_="poster")
poster = poster.find("img")["src"]
poster = poster.split('?')
new_size = '?type=m203_290_2'
poster = poster[0] + new_size

# 3. staff & staff_image
people = soup.find_all("a", class_="thumb_people")
# 영화 감독 + 주연배우 5명 순서대로 list에 담겨져 있음
staff = []
thumb_staff = []
for i in people:
    thumb_staff.append(i.find("img")["src"])
    staff.append(i.find("img")["alt"])


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

# count = soup.find("p", class_="count")[0].text

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


viewer_img = soup.find("div", class_="viewer_img").find("img")["src"]


movie_detail = {
    "overview" : overview,
    "poster" : poster,
    "staff" : staff,
    "thumb_staff" : thumb_staff,
    "netizen_score" : netizen_score,
    "special_score" : special_score,
    "running_time" : running_time,
    "genre" : genre,
    "grade" : grade,
    "download_url" : download_url,
    "best_line1_character" : best_line1_character,
    "best_line1" : best_line1,
    "best_line2_character" : best_line2_character,
    "best_line2" : best_line2,
    "relate_movies" : relate_movies,
    "relate_movies_thumb" : relate_movies_thumb,
    "aka_info" : aka_info,
    "viewer_img" : viewer_img
}

# MovieDetail(
#     movie_id=''
#     overview=movie_detail['overview'],
#     poster=movie_detail['poster'],
#     staff1=movie_detail['staff1'],
#     staff2=movie_detail['staff2'],
#     staff3=movie_detail['staff3'],
#     staff4=movie_detail['staff4'],
#     staff5=movie_detail['staff5'],
#     thumb_staff1=movie_detail['thumb_staff1'],
#     thumb_staff2=movie_detail['ovethumb_staff2rview'],
#     thumb_staff3=movie_detail['thumb_staff3'], 
#     thumb_staff4=movie_detail['thumb_staff4'],
#     thumb_staff5=movie_detail['thumb_staff5'],
#     netizen_score=movie_detail['netizen_score'],
#     special_score=movie_detail['special_score'],
#     running_time=movie_detail['running_time'],
#     genre=movie_detail['genre'],
#     grade=movie_detail['grade'],
#     download_url=movie_detail['download_url'],
#     best_line1_character=movie_detail['best_line1_character'],
#     best_line1=movie_detail['best_line1'],
#     best_line2_character=movie_detail['best_line2_character'],
#     best_line2=movie_detail['best_line2'],
#     relate_movie1 =movie_detail['relate_movie1'],
#     relate_movie2 =movie_detail['relate_movie2'],
#     relate_movie3 =movie_detail['relate_movie3'],
#     relate_movie4 =movie_detail['relate_movie4'],
#     relate_movie5 =movie_detail['relate_movie5'],
#     relate_movies_thumb1 =movie_detail['relate_movies_thumb1'],
#     relate_movies_thumb2 =movie_detail['relate_movies_thumb2'],
#     relate_movies_thumb3=movie_detail['relate_movies_thumb3'],
#     relate_movies_thumb4 =movie_detail['overrelate_movies_thumb4view'],
#     relate_movies_thumb5 =movie_detail['relate_movies_thumb5'],
#     aka_info =movie_detail['aka_info'],
#     viewer_img =movie_detail['viewer_img'],
# )

pprint(movie_detail)