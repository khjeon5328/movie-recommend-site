from django.shortcuts import render
from .models import Movie
from .models import MovieDetail
import requests
import json
from pprint import pprint


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def movies(request):
    MOVIE_BOX_OFFICE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    targetDt = '20180428'
    key = 'afcff8156929eef627192c4cc730285c'

    payload = {'key': key, 'targetDt': targetDt}
    r = requests.get(MOVIE_BOX_OFFICE_URL, params=payload)
    r_dict = r.json()
    movies = r_dict["boxOfficeResult"]["dailyBoxOfficeList"]

    for movie in movies:
        Movie(
            movie_name=movie['movieNm'],
            rank=movie['rank'],
            # False == old
            rank_old_and_new=movie['rankOldAndNew'],
            open_dt=movie['openDt'],
            sales_share=movie['salesShare'],
            sales_change=movie['salesChange'],
            sales_acc=movie['salesAcc'],
            audi_cnt=movie['audiCnt'],
            audi_change=movie['audiChange'],
            audi_acc=movie['audiAcc'],
            scrn_cnt=movie['scrnCnt'],
            show_cnt=movie['showCnt']
        ).save()
    return

def test(request):
    # naverMovie('테넷')
    req = requests.get('https://movie.naver.com/movie/search/result.nhn?query=%ED%85%8C%EB%84%B7&section=all&ie=utf8')
    ## HTML 소스 가져오기
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    cl = soup.find("p", class_="result_thumb").find("a")["href"]
    print(cl)
    return render(request,'index.html')


def movieDetail(request):
    boxoffice_movies = Movie.objects.all()
    for box_movie in boxoffice_movies:
        keyword = box_movie.movie_name
        naverMovie(keyword)

def naverMovie(keyword):
    try:
        driver = webdriver.Chrome("C:\\Users\\grey\\Downloads\\chromedriver_win32\\chromedriver.exe")
        driver.get("https://movie.naver.com/")
        elem = driver.find_element_by_class_name("ipt_tx_srch")
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        
        soup.select(
            '#old_content > ul:nth-child(4) > li > dl > dt > a'
        )["href"]
        continue_link = driver.find_element_by_partial_link_text(keyword)
        continue_link.click()
    
    except e:
        print('selenium error')
        return

    finally:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            print(soup)
        finally:
            overview = soup.select(
                '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p'
            )[0].text.replace('\xa0', '')
            # overview = soup.select(".con_tx")[0].text.replace('\xa0', '')
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
                "aka_info" : aka_info,
                "viewer_img" : viewer_img
            }

            for i in range(5):
                movie_detail[f'staff{i+1}'] = staff[i]
                movie_detail[f'thumb_staff{i+1}'] = thumb_staff[i]
                movie_detail[f'relate_movie{i+1}'] = relate_movies[i]
                movie_detail[f'relate_movies_thumb{i+1}'] = relate_movies_thumb[i]

            MovieDetail(
                movie_id=Movie.objects.get(pk=1),
                overview=movie_detail['overview'],
                poster=movie_detail['poster'],
                staff1=movie_detail['staff1'],
                staff2=movie_detail['staff2'],
                staff3=movie_detail['staff3'],
                staff4=movie_detail['staff4'],
                staff5=movie_detail['staff5'],
                thumb_staff1=movie_detail['thumb_staff1'],
                thumb_staff2=movie_detail['thumb_staff2'],
                thumb_staff3=movie_detail['thumb_staff3'], 
                thumb_staff4=movie_detail['thumb_staff4'],
                thumb_staff5=movie_detail['thumb_staff5'],
                netizen_score=movie_detail['netizen_score'],
                special_score=movie_detail['special_score'],
                running_time=movie_detail['running_time'],
                genre=movie_detail['genre'],
                grade=movie_detail['grade'],
                download_url=movie_detail['download_url'],
                best_line1_character=movie_detail['best_line1_character'],
                best_line1=movie_detail['best_line1'],
                best_line2_character=movie_detail['best_line2_character'],
                best_line2=movie_detail['best_line2'],
                relate_movie1 =movie_detail['relate_movie1'],
                relate_movie2 =movie_detail['relate_movie2'],
                relate_movie3 =movie_detail['relate_movie3'],
                relate_movie4 =movie_detail['relate_movie4'],
                relate_movie5 =movie_detail['relate_movie5'],
                relate_movies_thumb1 =movie_detail['relate_movies_thumb1'],
                relate_movies_thumb2 =movie_detail['relate_movies_thumb2'],
                relate_movies_thumb3=movie_detail['relate_movies_thumb3'],
                relate_movies_thumb4 =movie_detail['relate_movies_thumb4'],
                relate_movies_thumb5 =movie_detail['relate_movies_thumb5'],
                aka_info =movie_detail['aka_info'],
                viewer_img =movie_detail['viewer_img'],
            ).save()

            pprint(movie_detail)
            return