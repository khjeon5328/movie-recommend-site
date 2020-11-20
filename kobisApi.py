import requests
import json
from pprint import pprint
# Create your views here.
   
   
MOVIE_BOX_OFFICE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'


# 20200707
# 2019
# 20180428
# 2017
# 2016

targetDt = '20180428'
key = 'afcff8156929eef627192c4cc730285c'

payload = {'key': key, 'targetDt': targetDt}
r = requests.get(MOVIE_BOX_OFFICE_URL, params=payload)
r_dict = r.json()
movie = r_dict["boxOfficeResult"]["dailyBoxOfficeList"][0]

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
)



pprint(movie)