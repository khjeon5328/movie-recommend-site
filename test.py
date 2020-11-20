from bs4 import BeautifulSoup
import requests

req = requests.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code=136900')
## HTML 소스 가져오기
html = req.text

soup = BeautifulSoup(html, 'html.parser')


relate_movies = []
relate_movies_thumb = []

relate_movie = soup.find("ul", class_="thumb_link_mv").find_all("li")

print(len('https://s.pstatic.net/movie.phinf/20111223_44/1324635585945KDOJ5_JPEG/movie_image.jpg?type=m133_190_2'))
