from django.shortcuts import render

import requests
import json
from pprint import pprint
# Create your views here.


def movies(request):


    # 영진위
    # MOVIE_BOX_OFFICE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'

    # targetDt = '20180428'
    # key = 'afcff8156929eef627192c4cc730285c'
    
    # payload = {'key': key, 'targetDt': targetDt}
    # r = requests.get(MOVIE_BOX_OFFICE_URL, params=payload)
    # r_dict = r.json()
    # pprint(r_dict)


    # naver api
    NAVER_API_URL = 'https://openapi.naver.com/v1/search/movie.json'
    client_id = 'pOiVdybgL25JcgtbgRYe'
    client_secret = 'rz1GFJSd9l'
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    payload = {'query': '어벤져스'}
    r = requests.get(NAVER_API_URL, params=payload, headers=headers)
    r_dict = r.json()
    pprint(r_dict)

    context = {

    }
    return render(request, 'movies/movies.html', context)