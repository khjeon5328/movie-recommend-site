from django.shortcuts import render
from .models import Movie
from .models import MovieDetail
import requests
import json
from pprint import pprint


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def movies(request):
    MOVIE_BOX_OFFICE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    # 20130302 입학
    # 20150927 추석
    # 20170213 발렌타인
    # 20191225 크리스마스
    # 20180428 어벤져스
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
            target_dt=targetDt,
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
    return render(request, 'index.html')

def test(request):
    Movie.objects.all().delete()
    return render(request,'index.html')




def naverMovie(keyword, movie_id):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome("C:\\Users\\grey\\Downloads\\chromedriver_win32\\chromedriver.exe", options=options)
    try:
        driver.get("https://movie.naver.com/")
        elem = driver.find_element_by_class_name("ipt_tx_srch")
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        continue_link = driver.find_element_by_xpath("//*[@id='old_content']/ul[2]/li/dl/dt/a").click()
    
    except e:
        print('selenium error')
        return

    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)
    
        overview = soup.select(
            '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p'
        )
        if overview:
            overview = overview[0].text.replace('\xa0', '')
        else:
            overview = "null"
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
        while len(staff) < 5:
            staff.append('null')
        while len(thumb_staff) < 5:
            thumb_staff.append('null')


        netizen_score = soup.select(
            "#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.netizen_score > div > div > em"
        )
        if netizen_score:
            netizen_score = netizen_score[0].text
        else:
            netizen_score = -1

        special_score = soup.select(
            "#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.special_score > div > div > em"
        )
        if special_score:
            special_score = special_score[0].text
        else:
            special_score = -1


        running_time = soup.select(
            "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)"
        )
        if running_time:
            running_time = running_time[0].text
        else:
            running_time = "null"

        genre = soup.select(
            "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a:nth-child(1)"
        )
        if genre:
            genre = genre[0].text
        else:
            genre = "null"

        grade = soup.select(
            "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a"
        )
        if grade:
            grade = grade[0].text
        else:
            grade = "null"


        download_url = soup.find("a",class_="btn_dnld")
        if download_url:
            download_url = download_url["href"]
        else:
            download_url = "null"
        # count = soup.find("p", class_="count")[0].text

        best_line1_character = soup.select(
            '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(1) > div > em > span'
        )
        if best_line1_character:
            best_line1_character = best_line1_character[0].text
        else:
            best_line1_character = 'null'

        best_line1 = soup.select(
            '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(1) > div > div > strong'
        )
        if best_line1:
            best_line1 = best_line1[0].text
        else:
            best_line1 = 'null'


        best_line2_character = soup.select(
            '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(2) > div > em > span'
        )
        if best_line2_character:
            best_line2_character = best_line2_character[0].text
        else:
            best_line2_character = 'null'

        best_line2 = soup.select(
            '#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(2) > div > div > strong'
        )
        if best_line2:
            best_line2 = best_line2[0].text
        else:
            best_line2 = 'null'

        relate_movie = soup.find("ul", class_="thumb_link_mv").find_all("li")
        # 5개가 default
        relate_movies = []
        relate_movies_thumb = []

        for i in relate_movie:
            relate_movies.append(i.find("img")["alt"])
            relate_movies_thumb.append(i.find("img")["src"].strip(' \t\n\r'))

        # 잘 알려진 keyword list 형태로 구현
        aka_info = soup.find("div", class_="aka_info")
        if aka_info:
            aka_info = aka_info.find("p").text.split('|')
            for i in range(len(aka_info)):
                aka_info[i] = aka_info[i].strip(' \x06\t\n\r')
        else:
            aka_info ='null'


        viewer_img = soup.find("div", class_="viewer_img")
        if viewer_img:
            viewer_img = viewer_img.find("img")["src"]
         
        else:
            viewer_img ='null'


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
            movie=Movie.objects.get(pk=movie_id),
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

def movieDetail(request):
    boxoffice_movies = Movie.objects.all()
    for box_movie in boxoffice_movies:
        keyword = box_movie.movie_name
        movie_id = box_movie.id
        naverMovie(keyword, movie_id)
        time.sleep(2)
    # naverMovie('인턴', 4)
    return render(request, 'index.html')