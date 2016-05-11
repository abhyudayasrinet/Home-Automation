import requests
from bs4 import BeautifulSoup

url = "https://news.google.co.in"

r = requests.get(url)

html = r.content
soup = BeautifulSoup(html, "html.parser")

headlines = soup.findAll("span",{"class":"titletext"})

for headline in headlines:
    print(headline.text)