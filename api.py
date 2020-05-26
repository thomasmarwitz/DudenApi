# python -i api.py == exec(open("api.py").read())
## Scraping all german Words!
## [tag for tag in soup.find_all("a", multi_valued_attributes=None) if tag.get("class") == "hookup__link"]
import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.duden.de/rechtschreibung/Haus")

soup = BeautifulSoup(response.text, "lxml", multi_valued_attributes=None)

for tag in soup.find_all("div", multi_valued_attributes=None):
    try:
        if tag["class"] == "division ":
            #print(tag["id"])
            pass
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

# BEDEUTUNG
tag = TAGS[0] # filter via ID

# Access Content
content = tag.contents
content[0] = " "
title = content[1].h2 # enthält Überschrift -> Perfekt nutzbar!
print(title.get_text())

# Rechtschreibung Bsp!
rechtschr = content[2]
# <dl class=tuple>


key = rechtschr.dt.get_text()
val = rechtschr.dd.get_text()
print(f"{key} - {val}")

bsp_box = content[3]
txt = [tag.get_text() for tag in bsp_box.find_all("li")]

print("\n---\n", "\n".join(txt))

import sys
sys.exit()

actual_content = content[2]

bedeutung_1 = actual_content.li # find_all("li")

note_title = bedeutung_1.div # Text-Container -> Bedeutung
print(note_title.get_text())
# <dl class="note">
note = bedeutung_1.dl    # find_all("dl") tag["class"]="note"
# <dt class="note__title">Beispiele</dt>
bsp =  note.find_all("li")
for a in bsp:
    print("-", a.get_text())
