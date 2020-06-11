# melon-chartbot
이 프로젝트는 멜론 차트를 쉽게 파싱할 수 있게끔 제작되었습니다.

# 0. 필요한 소프트웨어
- python (3.8)

# 1. 필요한 모듈
```
pip install numpy
pip install matplotlib
pip install requests
pip install bs4
```

# 2. 예시 코드
```python
import melonapi

#ex1) 실시간 그래프
realgraph = melonapi.Realgraph()
datetime = realgraph.getDatetime()
print(datetime.strftime("%Y%m%d %H:%M"))
timelist = realgraph.getTimelist()
print(timelist)
data = realgraph.getChartdata()
for d in data:
    print(d.currank, d.songname, d.data)
realgraph.getGraph(font_path="/Users/guysome/Library/Fonts/NanumBarunGothic.ttf", img_path="realgraph.png")


realgraph.refresh()


#ex2) 실시간 차트
realchart = melonapi.Realchart()
datetime = realchart.getDatetime()
print(datetime.strftime("%Y%m%d %H:%M"))
data = realchart.getChartdata()
for d in data:
    print(d.currank, d.updown, d.rankgap, d.songname)


realchart.refresh()


#ex3) 5분 차트
fivechart = melonapi.Fivechart()
datetime = fivechart.getDatetime()
print(datetime.strftime("%Y%m%d %H:%M"))
data = fivechart.getChartdata()
for d in data:
    print(d.songname, d.data)
fivechart.getGraph(font_path="/Users/guysome/Library/Fonts/NanumBarunGothic.ttf", img_path="fivechart.png")


fivechart.refresh()

#ex4) 이용자수
countnum = melonapi.Countnum()
datetime = countnum.getDatetime()
print(datetime.strftime("%Y%m%d %H:%M"))
data = countnum.getChartdata()
for d in data:
    print(d.songname, d.artist, d.songid, d.count, d.male, d.female, d.age10, d.age20, d.age30, d.age40, d.age50, d.age60)
    print(d.getMale(), d.getFemale(), d.getAge10(), d.getAge20(), d.getAge30(), d.getAge40(), d.getAge50(), d.getAge60())
countnum.refresh()
```

# 3. Realchart Class
### Inner Class
Song Class
- currank : 순위 (int)
- pastrank : 전시간대 순위 (int)
- rankgap : 순위 변동 (int)
- updown : 순위 변동 유형 (str) / UP(상승), DOWN(하락), NEW(진입), NONE(유지)
- songname : 곡명 (str)
- artist : 가수명 (str)
- albumimg : 앨범 이미지 (str, url)
- songid : 곡 코드 (int)

### Method
- refresh() None : 차트를 갱신합니다.
- getHour() int : 불러온 차트의 시간을 return 합니다.
- getDate() int : 불러온 차트의 날짜를 8자리의 정수로 return 합니다.
- getDatetime() datetime : 불러온 차트의 날짜와 시간을 datetime 객체로 return 합니다.
- getChartdata() list of Song : 불러온 차트의 데이터를 Song 객체의 list 형태로 return 합니다.


# 4. Realgraph Class
### Inner Class
Song Class
- currank : 순위 (int)
- data : 실수치 (list of float)
- songname : 곡명 (str)

### Method
- refresh() None : 차트를 갱신합니다.
- getHour() int : 불러온 차트의 시간을 return 합니다.
- getDate() int : 불러온 차트의 날짜를 8자리의 정수로 return 합니다.
- getDatetime() datetime : 불러온 차트의 날짜와 시간을 datetime 객체로 return 합니다.
- getChartdata() list of Song : 불러온 차트의 데이터를 Song 객체의 list 형태로 return 합니다.
- getTimelist() list of datetime : 불러온 차트의 x축을 datetime 객체의 list 형태로 return 합니다.
- getGraph(font_path, img_path) None : 불러온 차트를 matplotlib를 이용해 그래프를 생성 및 저장합니다.

# 5. Fivechart Class
### Inner Class
Song Class
- songid : 곡 코드 (int)
- data : 실수치 (list of float)
- songname : 곡명 (str)

### Method
- refresh() None : 차트를 갱신합니다.
- getMinute() int : 불러온 차트의 분을 return 합니다.
- getHour() int : 불러온 차트의 시간을 return 합니다.
- getDate() int : 불러온 차트의 날짜를 8자리의 정수로 return 합니다.
- getDatetime() datetime : 불러온 차트의 날짜와 시간을 datetime 객체로 return 합니다.
- getChartdata() list of Song : 불러온 차트의 데이터를 Song 객체의 list 형태로 return 합니다.
- getGraph(font_path, img_path) None : 불러온 차트를 matplotlib를 이용해 그래프를 생성 및 저장합니다.

# 6. Countnum Class
### Inner Class
Song Class
- songname : 곡명 (str)
- artist : 가수명 (str)
- count : 이용자수 (int)
- male : 남성 비율 (float)
- female : 여성 비율 (float)
- age10 : 10대 비율 (float)
- age20 : 20대 비율 (float)
- age30 : 30대 비율 (float)
- age40 : 40대 비율 (float)
- age50 : 50대 비율 (float)
- age60 : 60대 비율 (float)
- getMale() int : 남성 이용자수
- getFemale() int : 여성 이용자수
- getAge10() int : 10대 이용자수
- getAge20() int : 20대 이용자수
- getAge30() int : 30대 이용자수
- getAge40() int : 40대 이용자수
- getAge50() int : 50대 이용자수
- getAge60() int : 60대 이용자수

### Method
- refresh() None : 차트를 갱신합니다.
- getHour() int : 불러온 차트의 시간을 return 합니다.
- getDate() int : 불러온 차트의 날짜를 8자리의 정수로 return 합니다.
- getDatetime() datetime : 불러온 차트의 날짜와 시간을 datetime 객체로 return 합니다.
- getChartdata() list of Song : 불러온 차트의 데이터를 Song 객체의 list 형태로 return 합니다.

# 7. Dailychart Class
### Inner Class
Song Class
- currank : 순위 (int)
- pastrank : 전시간대 순위 (int)
- rankgap : 순위 변동 (int)
- updown : 순위 변동 유형 (str) / UP(상승), DOWN(하락), NEW(진입), NONE(유지)
- songname : 곡명 (str)
- artist : 가수명 (str)
- albumimg : 앨범 이미지 (str, url)
- songid : 곡 코드 (int)

### Method
- refresh() None : 차트를 갱신합니다.
- getDate() date : 불러온 차트의 날짜를 date 객체로 return 합니다.
- getChartdata() list of Song : 불러온 차트의 데이터를 Song 객체의 list 형태로 return 합니다.

# 8. Detailinfo Class
- currank : 일간 차트 순위 (int)
- songname : 곡명 (str)
- artist : 가수명 (str)
- albumimg : 앨범 이미지 (str)
- songid : 곡 코드 (int)
- date : 리포트 갱신 일자 (date)
- count : 이용자수 (int)
- male : 남성 비율 (float)
- female : 여성 비율 (float)
- age10 : 10대 비율 (float)
- age20 : 20대 비율 (float)
- age30 : 30대 비율 (float)
- age40 : 40대 비율 (float)
- age50 : 50대 비율 (float)
- age60 : 60대 비율 (float)
- firstrankinfo : 최고 순위, 1위 횟수 등 (str)
- recordlist : 이 곡의 기록 목록 (list)

### Method
- getMale() int : 남성 이용자수
- getFemale() int : 여성 이용자수
- getAge10() int : 10대 이용자수
- getAge20() int : 20대 이용자수
- getAge30() int : 30대 이용자수
- getAge40() int : 40대 이용자수
- getAge50() int : 50대 이용자수
- getAge60() int : 60대 이용자수
- refresh() None : 곡 상세정보를 갱신합니다.
- getData() Song : 불러온 곡 상세정보 데이터를 Song 객체로 return 합니다.
