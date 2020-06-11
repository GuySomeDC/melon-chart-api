import requests
from bs4 import BeautifulSoup
from datetime import *
import re
import json


class Realchart:
    class Song:
        def __init__(self, data):
            self.currank = int(data["CURRANK"])
            self.pastrank = int(data["PASTRANK"])
            self.rankgap = int(data["RANKGAP"])
            self.updown = data["UPDOWN"]
            self.songname = data["SONGNAME"]
            self.artist = data["ARTIST"]
            self.albumimg = data["ALBUMIMG"]
            self.songid = int(data["SONGID"])

    def __init__(self):
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        self.refresh()

    def refresh(self):
        self._result = self._session.get("https://www.melon.com/chart/index.htm", timeout=3)

    def getHour(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()[:2])

    def getDate(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", ""))

    def getDatetime(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        date = soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", "-")
        hour = soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()
        return datetime.strptime(date + " " + hour, "%Y-%m-%d %H:%M")

    def getChartdata(self):
        data = []
        soup = BeautifulSoup(self._result.text, "html.parser")
        lst50 = soup.find_all("tr", {"class": "lst50"})
        lst100 = soup.find_all("tr", {"class": "lst100"})
        for l in lst50 + lst100:
            d = {
                "CURRANK": int(l.find("span", {"class": "rank"}).text.strip()),
                "SONGNAME": l.find("div", {"class": "rank01"}).text.strip(),
                "ARTIST": l.find("div", {"class", "rank02"}).text.strip(),
                "SONGID": l["data-song-no"],
                "ALBUMIMG": l.find("img")["src"]
            }
            try:
                d["UPDOWN"] = "UP"
                d["RANKGAP"] = int(l.find("span", {"class": "up"}).text.strip())
                d["PASTRANK"] = d["CURRANK"] + d["RANKGAP"]
            except:
                try:
                    d["UPDOWN"] = "DOWN"
                    d["RANKGAP"] = int(l.find("span", {"class": "down"}).text.strip())
                    d["PASTRANK"] = d["CURRANK"] - d["RANKGAP"]
                except:
                    try:
                        d["UPDOWN"] = "NONE"
                        d["RANKGAP"] = int(l.find("span", {"class": "rank_wrap"}).find("span", {"class": "none"}).text.strip().replace("순위 동일", "0"))
                        d["PASTRANK"] = d["CURRANK"]
                    except:
                        d["UPDOWN"] = "NEW"
                        d["RANKGAP"] = 0
                        d["PASTRANK"] = 0
            data.append(self.Song(d))

        return data


class Realgraph:
    class Song:
        def __init__(self, data):
            self.currank = int(data["index"]) + 1
            self.data = data["data"]
            self.songname = data["name"]

    def __init__(self):
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        self.refresh()

    def refresh(self):
        self._result = self._session.get("https://www.melon.com/chart/index.htm", timeout=3)

    def getHour(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()[:2])

    def getDate(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", ""))

    def getDatetime(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        date = soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", "-")
        hour = soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()
        return datetime.strptime(date + " " + hour, "%Y-%m-%d %H:%M")

    def getChartdata(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        script = soup.find('script', text=re.compile('var series ='))
        values = re.findall(r'var series =(.*?);', script.text, re.S)
        value = json.loads(values[0].replace('type', '"type"').replace('name', '"name"').replace('data', '"data"').replace('index', '"index"').replace("\n", "").replace("\t", ""))
        data = []
        for v in value:
            data.append(self.Song(v))
        return data

    def getTimelist(self):
        now = self.getDatetime()
        start = self.getDatetime() - timedelta(hours=23)
        data = []
        while start <= now:
            data.append(start)
            if start.hour == 1:
                start += timedelta(hours=5)
            start += timedelta(hours=1)

        return data

    def getGraph(self, font_path="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf", img_path="realgraph.png"):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager, rc

        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)
        chartdata = self.getChartdata()
        graphdatalist = [c.data for c in chartdata]
        timelist = [c.strftime("%H") for c in self.getTimelist()]
        songname = [c.songname for c in chartdata]
        maxvalue = 0
        for gdata in graphdatalist:
            for g in gdata:
                try:
                    if g > maxvalue:
                        maxvalue = g
                except:
                    continue
        maxvalue += 0.5
        if maxvalue < 7:
            maxvalue = 7
        fig = plt.figure(figsize=(11, 7))
        fig.patch.set_facecolor('#424e67')
        ax = fig.add_subplot(111)
        ax.patch.set_facecolor('#424e67')
        plt.axis([0, len(graphdatalist[0]) - 1, 0, maxvalue])
        plt.rcParams['lines.linewidth'] = 3
        clr = ['#a7e52e', '#f6894e', '#59afe5']
        if maxvalue > 7:
            plt.axhline(y=7.0, color='w', linewidth=1)
        for i in range(0, 3):
            plt.plot(timelist, graphdatalist[i], label=songname[i], color=clr[i])
            for q, txt in enumerate(graphdatalist[i]):
                try:
                    if graphdatalist[i][q] != None:
                        if graphdatalist[i][q] >= 7.0:
                            ax.annotate('●', (timelist[q], graphdatalist[i][q]), color=clr[i], fontsize=9, ha='center', va='center')
                        if graphdatalist[i][q] != 0:
                            if i == 0:
                                ax.annotate(round(txt, 3), (timelist[q], graphdatalist[i][q]), color=clr[i], fontsize=14)
                            else:
                                if abs(graphdatalist[i - 1][q] - graphdatalist[i][q]) <= 0.4:
                                    ax.annotate(round(txt, 3), (timelist[q], graphdatalist[i][q] - 0.2), color=clr[i], fontsize=14)
                                else:
                                    ax.annotate(round(txt, 3), (timelist[q], graphdatalist[i][q]), color=clr[i], fontsize=14)
                except:
                    if graphdatalist[i][q] >= 7.0:
                        ax.annotate('●', (timelist[q], graphdatalist[i][q]), color=clr[i], fontsize=9, ha='center', va='center')
                    else:
                        ax.annotate(round(txt, 3), (timelist[q], graphdatalist[i][q]), color=clr[i], fontsize=14)
        plt.grid(color='#687185', linestyle='--', axis='x')
        plt.legend(fontsize=8.5)
        plt.title('[' + str(self.getDatetime().strftime("%Y%m%d %H:00")) + '] 멜론 실시간 그래프 by 가이섬.com', fontsize=15, color='#ffffff')
        plt.subplots_adjust(left=0.02, right=0.955, top=0.955, bottom=0.04)
        plt.yticks(np.arange(0, maxvalue, 1))
        ax.tick_params(colors='#ffffff')
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        plt.savefig(img_path, facecolor=fig.get_facecolor())
        plt.close("all")


class Fivechart:
    class Song:
        def __init__(self, d):
            self.data = d["data"]
            self.songname = d["title"]
            self.songid = int(d["name"])

    def __init__(self):
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        self.refresh()

    def refresh(self):
        self._result = self._session.get("https://www.melon.com/chart/index.htm", timeout=3)
        self._data = self._parseFive()

    def getLength(self):
        return self.getDatetime().minute // 5 + 1

    def getMinute(self):
        return self.getDatetime().minute

    def getHour(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()[:2])

    def getDate(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", ""))

    def getDatetime(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        date = soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", "-")
        hour = soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()[:2]
        minute = (len(self._data[0].data) - 1) * 5
        if minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)
        return datetime.strptime(date + " " + hour + ":" + minute, "%Y-%m-%d %H:%M")

    def _parseFive(self):
        songinfo = []
        soup = BeautifulSoup(self._result.text, 'html.parser')
        tit = soup.find_all('span', {'class': 'tit'})
        script = soup.find('script', text=re.compile('fiveSeries\.push'))
        values = re.findall(r'fiveSeries\.push\((.*?)\);', script.text, re.S)
        wrap_info = soup.find_all('div', {'class': 'wrap_song_info ellipsis'})
        songtitle = {}
        for wrap in wrap_info:
            songid = re.search(r'playSong\(\'(\d*)\'\,\'(.*?)\'\)', str(wrap), re.S)
            songtitle[songid.group(2)] = wrap.find('span', {'class': 'tit'}).text.strip()

        for i in range(0, len(values)):
            new_songinfo = {}
            new_songinfo['title'] = tit[i + 3].text.strip()
            value = json.loads(values[i].replace('type', '"type"').replace('name', '"name"').replace('data', '"data"').replace('\t', '').replace('\n', '').replace("'', ", ''))
            new_songinfo['data'] = value['data']
            new_songinfo['name'] = value['name']
            new_songinfo['title'] = songtitle[new_songinfo['name']]
            songinfo.append(self.Song(new_songinfo))
        return songinfo

    def getChartdata(self):
        return self._data

    def getGraph(self, font_path="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf", img_path="fivechart.png"):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager, rc

        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)
        clr = ['#a7e52e', '#f6894e', '#59afe5', '#fd7db9', '#c998ff', '#39c5c2']

        strtoday = str(self.getDatetime().strftime("%Y%m%d %H:%M"))
        max = 0
        for song in self._data:
            for val in song.data:
                if val > max:
                    max = val
        max += 1
        fig = plt.figure(figsize=(8.5, 5.1))
        ax = fig.add_subplot(111)
        ax.patch.set_facecolor('#424e67')
        plt.axis([0, 60, 0, max])
        plt.rcParams['lines.linewidth'] = 3
        minute = self.getDatetime().minute + 5
        X = np.arange(0, minute, 5)
        sorted_songinfo = sorted(self._data, key=lambda k: k.data[len(k.data) - 1], reverse=True)
        for i in range(0, len(self._data)):
            for j in range(0, len(sorted_songinfo)):
                if self._data[i].songid == sorted_songinfo[j].songid:
                    plt.plot(X, self._data[i].data, label=self._data[i].songname, color=clr[i])
                    for q, txt in enumerate(self._data[i].data):
                        if j == 0:
                            ax.annotate(round(txt, 2), (X[q], self._data[i].data[q]), color=clr[i], fontsize=15)
                        else:
                            if abs(sorted_songinfo[j - 1].data[q] - sorted_songinfo[j].data[q]) <= 0.4:
                                ax.annotate(round(txt, 2), (X[q], self._data[i].data[q] - 0.3), color=clr[i], fontsize=15)
                            else:
                                ax.annotate(round(txt, 2), (X[q], self._data[i].data[q]), color=clr[i], fontsize=15)
                    break
        plt.grid()
        plt.legend(fontsize=8.5)
        plt.title('[' + str(strtoday) + '] 멜론 5분 차트 by 가이섬.com', fontsize=15)
        plt.subplots_adjust(left=0.02, right=0.98, top=0.950, bottom=0.05)
        plt.savefig(img_path)
        plt.close("all")


class Countnum:
    class Song:
        def __init__(self, d):
            self.songname = d["SONGNAME"]
            self.artist = d["ARTIST"]
            self.count = int(d["COUNT"])
            self.male = float(d["MALE"])
            self.female = float(d["FEMALE"])
            self.age10 = float(d["AGE10"])
            self.age20 = float(d["AGE20"])
            self.age30 = float(d["AGE30"])
            self.age40 = float(d["AGE40"])
            self.age50 = float(d["AGE50"])
            self.age60 = float(d["AGE60"])
            self.songid = int(d["SONGID"])
            self.albumimg = d["ALBUMIMG"]

        def getMale(self):
            return round(self.count * self.male * 0.01)

        def getFemale(self):
            return round(self.count * self.female * 0.01)

        def getAge10(self):
            return round(self.count * self.age10 * 0.01)

        def getAge20(self):
            return round(self.count * self.age20 * 0.01)

        def getAge30(self):
            return round(self.count * self.age30 * 0.01)

        def getAge40(self):
            return round(self.count * self.age40 * 0.01)

        def getAge50(self):
            return round(self.count * self.age50 * 0.01)

        def getAge60(self):
            return round(self.count * self.age60 * 0.01)

    def __init__(self):
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        self.refresh()

    def refresh(self):
        self._result = self._session.get("https://www.melon.com/chart/index.htm", timeout=3)

    def getHour(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()[:2])

    def getDate(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        return int(soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", ""))

    def getDatetime(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        date = soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip().replace(".", "-")
        hour = soup.find("span", {"class": "hhmm"}).find("span", {"class": "hour"}).text.strip()
        return datetime.strptime(date + " " + hour, "%Y-%m-%d %H:%M")

    def getChartdata(self):
        data = []
        soup = BeautifulSoup(self._result.text, "html.parser")
        count = soup.find_all("div", {"class": "count_num"})
        man = soup.find_all('li', {'class': 'man'})
        woman = soup.find_all('li', {'class': 'woman'})
        age = soup.find_all('ul', {'class': 'age_group'})
        btn_link = soup.find_all('div', {'class': 'btn_like'})
        tit = soup.find_all("span", {"class": "tit"})
        wrap_artist = soup.find_all("div", {"class": "song_info_cont2"})
        song_info_cont = soup.find_all("div", {"class": "song_info_cont"})
        try:
            for i in range(0, len(count)):
                data.append(self.Song({
                    "SONGNAME": tit[i].text.strip(),
                    "ARTIST": ", ".join([w.text.strip() for w in wrap_artist[i].find("div", {"class": "wrap_atist"}).find_all("span")]),
                    "SONGID": int(btn_link[i].find("button")["data-song-no"]),
                    "ALBUMIMG": song_info_cont[i].find("img")["src"],
                    "COUNT": int(count[i].find("em").text.strip().replace(",", "")),
                    "MALE": float(man[i]['style'].replace('width:', '').replace('%;','')),
                    "FEMALE": float(woman[i]['style'].replace('width:', '').replace('%;', '')),
                    "AGE10": float(age[i].find('li', {'class': 'nth1'}).find_all('span')[1].find('span')['style'].replace('height:', '').replace('%', '')),
                    "AGE20": float(age[i].find('li', {'class': 'nth2'}).find_all('span')[1].find('span')['style'].replace('height:', '').replace('%', '')),
                    "AGE30": float(age[i].find('li', {'class': 'nth3'}).find_all('span')[1].find('span')['style'].replace('height:', '').replace('%', '')),
                    "AGE40": float(age[i].find('li', {'class': 'nth4'}).find_all('span')[1].find('span')['style'].replace('height:', '').replace('%', '')),
                    "AGE50": float(age[i].find('li', {'class': 'nth5'}).find_all('span')[1].find('span')['style'].replace('height:', '').replace('%', '')),
                    "AGE60": float(age[i].find('li', {'class': 'nth6'}).find_all('span')[1].find('span')['style'].replace('height:', '').replace('%', '')),
                }))
        except:
            print("아직 이용자수가 갱신되지 않았습니다.")
            return None

        return data


class Dailychart:
    class Song:
        def __init__(self, data):
            self.currank = int(data["CURRANK"])
            self.pastrank = int(data["PASTRANK"])
            self.rankgap = int(data["RANKGAP"])
            self.updown = data["UPDOWN"]
            self.songname = data["SONGNAME"]
            self.artist = data["ARTIST"]
            self.albumimg = data["ALBUMIMG"]
            self.songid = int(data["SONGID"])

    def __init__(self):
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "AS40; Android 8.0.0; 4.8.3; SM-G935S"
        self.refresh()

    def refresh(self):
        self._result = self._session.get("https://www.melon.com/chart/day/index.htm", timeout=3)

    def getDate(self):
        soup = BeautifulSoup(self._result.text, "html.parser")
        date = soup.find("span", {"class": "yyyymmdd"}).find("span", {"class": "year"}).text.strip()
        return datetime.strptime(date, "%Y.%m.%d").date()

    def getChartdata(self):
        data = []
        soup = BeautifulSoup(self._result.text, "html.parser")
        lst50 = soup.find_all("tr", {"class": "lst50"})
        lst100 = soup.find_all("tr", {"class": "lst100"})
        for l in lst50 + lst100:
            d = {
                "CURRANK": int(l.find("span", {"class": "rank"}).text.strip()),
                "SONGNAME": l.find("div", {"class": "rank01"}).text.strip(),
                "ARTIST": l.find("div", {"class", "rank02"}).text.strip(),
                "SONGID": l["data-song-no"],
                "ALBUMIMG": l.find("img")["src"]
            }
            try:
                d["UPDOWN"] = "UP"
                d["RANKGAP"] = int(l.find("span", {"class": "up"}).text.strip())
                d["PASTRANK"] = d["CURRANK"] + d["RANKGAP"]
            except:
                try:
                    d["UPDOWN"] = "DOWN"
                    d["RANKGAP"] = int(l.find("span", {"class": "down"}).text.strip())
                    d["PASTRANK"] = d["CURRANK"] - d["RANKGAP"]
                except:
                    try:
                        d["UPDOWN"] = "NONE"
                        d["RANKGAP"] = int(l.find("span", {"class": "rank_wrap"}).find("span", {"class": "none"}).text.strip().replace("순위 동일", "0"))
                        d["PASTRANK"] = d["CURRANK"]
                    except:
                        d["UPDOWN"] = "NEW"
                        d["RANKGAP"] = 0
                        d["PASTRANK"] = 0
            data.append(self.Song(d))

        return data


class Detailinfo:
    def __init__(self, songid):
        self._songid = songid
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "AS40; Android 8.0.0; 4.8.3; SM-G935S"
        self.refresh()

    def refresh(self):
        params = {
            "cpId": "AS40",
            "cpKey": "14LNC3",
            "v": "4.1",
            "resolution": "4",
            "songId": self._songid
        }
        self._result = self._session.get("https://m.app.melon.com/song/detailInfo.json", params=params, timeout=3).json()["response"]
        try:
            self.currank = int(self._result["YESTERCHARTINFO"]["RANK"])
        except:
            self.currank = 1001
        self.count = int(self._result["STREPORT"]["LISTNERCNT"])
        self.male = float(self._result["STREPORT"]["MALE"])
        self.female = float(self._result["STREPORT"]["FEMALE"])
        self.age10 = float(self._result["STREPORT"]["AGE10"])
        self.age20 = float(self._result["STREPORT"]["AGE20"])
        self.age30 = float(self._result["STREPORT"]["AGE30"])
        self.age40 = float(self._result["STREPORT"]["AGE40"])
        self.age50 = float(self._result["STREPORT"]["AGE50"])
        self.age60 = float(self._result["STREPORT"]["AGE60"])
        self.songname = self._result["SONGNAME"]
        self.artist = ", ".join([d["ARTISTNAME"] for d in self._result["ARTISTLIST"]])
        self.albumimg = self._result["ALBUMINFO"]["ALBUMIMG"]
        self.songid = int(self._result["SONGID"])
        self.date = datetime.strptime(self._result["STREPORT"]["DATE"], "%Y.%m.%d").date()
        try:
            self._recordinfo = self._result["RECORDINFO"]
            self.recordlist = [r["RECORD"] for r in self._recordinfo["RECORDLIST"]]
        except:
            self._recordinfo = None
            self.recordlist = []
        try:
            self.firstrankinfo = self._result["YESTERCHARTINFO"]["FIRSTRANKINFO"]
        except:
            self.firstrankinfo = None

    def getMale(self):
        return round(self.count * self.male * 0.01)

    def getFemale(self):
        return round(self.count * self.female * 0.01)

    def getAge10(self):
        return round(self.count * self.age10 * 0.01)

    def getAge20(self):
        return round(self.count * self.age20 * 0.01)

    def getAge30(self):
        return round(self.count * self.age30 * 0.01)

    def getAge40(self):
        return round(self.count * self.age40 * 0.01)

    def getAge50(self):
        return round(self.count * self.age50 * 0.01)

    def getAge60(self):
        return round(self.count * self.age60 * 0.01)