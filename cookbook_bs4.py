from bs4 import BeautifulSoup
from example import html_doc as markup
#soup = BeautifulSoup(markup, "lxml")
with open("example.html") as fobj:
    soup = BeautifulSoup(fobj, "lxml")
