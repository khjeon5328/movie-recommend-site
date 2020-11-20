from bs4 import BeautifulSoup
import requests

req = requests.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code=136900')
## HTML 소스 가져오기
html = req.text

soup = BeautifulSoup(html, 'html.parser')




  overview = soup.select(
                '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p'
            )[0].text.replace('\xa0', '')

print(overview)