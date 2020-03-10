from melonapi import Fivechart
from datetime import *
import time

### crontab
### 5-55/5 0,7-23 * * * /usr/bin/python3 /root/melon-chart-api/example/fivechart_cron.py

if __name__ == "__main__":
    fc = Fivechart()
    now = datetime.now()
    while (now.minute // 5) * 5 != fc.getMinute():
        time.sleep(3)
        try:
            fc.refresh()
        except:
            print('Error')
            continue
        print('check:', datetime.now())
    fc.getGraph(font_path="/Users/guysome/Library/Fonts/NanumBarunGothic.ttf", img_path="fivechart.png")
    print('그래프 생성:', datetime.now())