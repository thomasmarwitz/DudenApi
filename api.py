# python -i api.py == exec(open("api.py").read())
## Scraping all german Words!
## [tag for tag in soup.find_all("a", multi_valued_attributes=None) if tag.get("class") == "hookup__link"]
# "\xa0" == " "

import requests
from bs4 import BeautifulSoup
import re
import pprint

class MyParser:
    """
    rechtschreibung:    Wort|tren|nung + evtl. Infobox
    bedeutungen:        Bedeutungen + Beispielboxen
    synonyme:           Liste an Wörtern
    grammatik:          Tabelle / Zeile
    kontext:             computer generierte Assoziationen
    """

    def __init__(self):
        self.store = {}

    @staticmethod
    def parse_field(text):
        """Extracts all words from a given string, returns them in a list.
        Everything that is not a char is discarded."""

        new = ""
        processing = True
        for c in text:
            if processing and c == "(":
                processing = False
            elif c == ")":
                processing = True
            elif processing:
                new += c

        comma_seperated = new.replace(";", ",")
        return [item.strip() for item in comma_seperated.split(",")]

    def process_rechtschreibung(self, tag):
        title = tag.h2.get_text() # enthält Überschrift
        body = []
        for key, val in zip(tag.find_all("dt"), tag.find_all("dd")):
            body.append((key.get_text(),
                         val.get_text()))

        box = [li_element.get_text() for li_element in tag.find_all("li")]

        self.store[tag['id']] = (body, box)

    def process_bedeutungen(self, tag):
        body = []
        elemente = [el for el in tag.find_all("li") if el.get("class") == "enumeration__item"]
        for el in elemente:
            note_title = el.div.get_text()
            body.append(note_title)

            notes = [note for note in el.find_all("dl") if note.get("class") == "note"]
            for note in notes:
                box = [li_element.get_text() for li_element in note.find_all("li")]

        self.store[tag['id']] = body

    def process_bedeutung(self, tag):
        title = tag.h2.get_text()
        body = tag.p.get_text()

        self.store[tag['id']] = body

    def process_synonyme(self, tag):
        title = tag.h2.get_text()
        body = []

        for li_element in tag.find_all("li"):
            raw_txt = li_element.get_text()
            # hier könnte man noch differenzieren...
            body.extend(MyParser.parse_field(raw_txt))

        self.store[tag['id']] = body

    def process_kontext(self, tag):
        if (cluster := getattr(tag, "figure")) and cluster["class"] == "tag-cluster__cluster":
            body = cluster.get_text().split(" ")
            self.store[tag['id']] = body

    def parse_tag(self, tag):
        func = getattr(self, f"process_{tag['id']}", self.default)
        func(tag)

    def default(self, tag):
        print(f"keine Operation: {tag['id']}")

def main(test=True):
    if test is True:
        response = requests.get("https://www.duden.de/rechtschreibung/Haus")
    else:
        desired_word = input("Wort?\n>> ").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
        # try casefold()
        response = requests.get(f"https://www.duden.de/rechtschreibung/{desired_word.casefold()}")
        # try title()
        if response.status_code != "200":
            response = requests.get(f"https://www.duden.de/rechtschreibung/{desired_word.title()}")

    # parse webresponse
    soup = BeautifulSoup(response.text, "lxml", multi_valued_attributes=None)
    # extract data-containing fields
    processable_tags = [tag for tag in soup.find_all("div", multi_valued_attributes=None) if tag.get("class") == "division "]
    # init parser & parse fields
    myparser = MyParser()
    for tag in processable_tags:
        myparser.parse_tag(tag)

    # prettify output
    pp = pprint.PrettyPrinter()
    pp.pprint(myparser.store)


if __name__ == "__main__":
    main(test=False)
