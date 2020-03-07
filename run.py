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

'''차트 갱신을 원할 경우
realgraph.refresh()
'''

#ex2) 실시간 차트
realchart = melonapi.Realchart()
datetime = realchart.getDatetime()
print(datetime.strftime("%Y%m%d %H:%M"))
data = realchart.getChartdata()
for d in data:
    print(d.currank, d.updown, d.rankgap, d.songname)

'''차트 갱신을 원할 경우
realchart.refresh()
'''

#ex3) 5분 차트
fivechart = melonapi.Fivechart()
datetime = fivechart.getDatetime()
print(datetime.strftime("%Y%m%d %H:%M"))
data = fivechart.getChartdata()
for d in data:
    print(d.songname, d.data)
fivechart.getGraph(font_path="/Users/guysome/Library/Fonts/NanumBarunGothic.ttf", img_path="fivechart.png")

'''차트 갱신을 원할 경우
fivechart.refresh()
'''