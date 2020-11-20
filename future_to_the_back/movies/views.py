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

    context = {

    }
    return render(request, 'movies/movies.html', context)


def moviedetail(request):
    return render(request, 'movies/moviedetail.html')
