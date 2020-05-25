# python -i api.py == exec(open("api.py").read())
import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.duden.de/rechtschreibung/Haus")

soup = BeautifulSoup(response.text, "lxml", multi_valued_attributes=None)

for tag in soup.find_all("div", multi_valued_attributes=None):
    try:
        if tag["class"] == "division ":
            print(tag["id"])
    except KeyError:
        pass
# yields
"""
rechtschreibung
bedeutungen
synonyme
herkunft
grammatik
wussten_sie_schon
aussprache
kontext
block-beforeafterblock-2
"""

TAGS = [tag for tag in soup.find_all("div", multi_valued_attributes=None) if tag.get("class") == "division "]

tag = TAGS[0] # filter via ID

# Access Content
content = tag.contents
content[0] = " "
content[1].h2.get_text() # enthält Überschrift -> Perfekt nutzbar!
actual_content = content[2]
bed_1 = actual_content.li # find_all("li")
bed_1.div.get_text() # Text-Container -> Bedeutung
