import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.duden.de/rechtschreibung/Haus")

soup = BeautifulSoup(response.text, "lxml", multi_valued_attributes=None)

for tag in soup.find_all("h2"):
    if tag["class"] == "division__title":
        print(tag.get_text())
