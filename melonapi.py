import requests
from bs4 import BeautifulSoup
from datetime import *

class Realchart:
    def __init__(self):
        self.datetime = datetime.now()
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"

    def refresh(self):
        url = ""
        self.result = self.session.get("https://www.melon.com/chart/index.htm")

    def getTime(self):
        soup = BeautifulSoup(self.result.text, "html.parser")
        return int(soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()[:2])