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

#ex5) 일간차트
dailychart = melonapi.Dailychart()
datetime = dailychart.getDatetime()
print(datetime.strftime("%Y%m%d"))
data = dailychart.getChartdata()
for d in data:
    print(d.currank, d.updown, d.rankgap, d.songname, d.songid)
    #ex6) 곡 상세정보
    detail = melonapi.Detailinfo(d.songid)
    detail_data = detail.getData()
    print(detail_data.currank, detail_data.count, detail_data.male, detail_data.female, detail_data.age10, detail_data.age20, detail_data.age30, detail_data.age40, detail_data.age50, detail_data.age60)