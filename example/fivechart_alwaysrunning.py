import melonapi
from datetime import *
import time

###### Always Running으로 사용할 경우 이 코드를 사용할 수 있습니다.
###### 그러나 crontab / 스케쥴러를 사용하길 권장합니다.

fc = melonapi.Fivechart()
oldMinute = 0
while True:
    try:
        print('check:', datetime.now())
        fc.refresh()
    except:
        print('Error')
        continue
    if datetime.now().minute // 5 + 1 == fc.getLength() and (datetime.now().minute // 5) * 5 != oldMinute:
        fc.getGraph(font_path="/Users/guysome/Library/Fonts/NanumBarunGothic.ttf", img_path="fivechart.png")
        oldMinute = (datetime.now().minute // 5) * 5
        print('그래프 생성:', datetime.now())

    time.sleep(3)