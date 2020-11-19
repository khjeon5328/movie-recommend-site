from bs4 import BeautifulSoup
import requests

req = requests.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code=136900')
## HTML 소스 가져오기
html = req.text

soup = BeautifulSoup(html, 'html.parser')

aka_info = soup.find("div", class_="aka_info").find("p").text.split('|')
# .strip(' \t\n\r')
for i in range(len(aka_info)):
    aka_info[i] = aka_info[i].strip(' \x06\t\n\r')
print(aka_info)