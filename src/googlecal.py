import os, datetime, pytz, json, pprint

import googleapiclient.discovery
import google.auth

import setting as ss

def getRequiredData(eventsList, calenderName):
    events = []

    calName = eventsList['summary']
    for ev in eventsList['items']:
        # 公開/非公開チェック
        if 'summary' in ev:
            title = ev['summary']
            if title.startswith('※'):
                continue
        else:
            title = 'Private'

        # 終日チェック
        if 'dateTime' in ev['start']:
            est = datetime.datetime.fromisoformat(ev['start']['dateTime'])
            eed = datetime.datetime.fromisoformat(ev['end']['dateTime'])
            isAllDay = False
        else:
            est = datetime.datetime.fromisoformat(ev['start']['date'])
            eed = datetime.datetime.fromisoformat(ev['end']['date'])
            isAllDay = True
        
        # 時間TimeZone調整
        jst = pytz.timezone('Asia/Tokyo')
        if 'timeZone' not in ev['start']:
            est = jst.localize(est)
        if 'timeZone' not in ev['end']:
            eed = jst.localize(eed)

        # 場所調整
        loc = ev['location'] if 'location' in ev else ''

        d = {
                'calendar': calName,
                'title': title,
                'start': est,
                'end': eed,
                'isAllDay': isAllDay,
                'location': loc,
                'id': title + str(est) + str(eed)
        }
        events.append(d)

    return events


def getEvents():
    """
    Googleカレンダーからイベント情報を取得する関数

    Returns:
        list: Googleカレンダーから取得したイベント情報のリスト。
        各イベントは辞書形式で表され、開始時刻でソートしてリストに入っている。
            'calendar': 'calendarのID', 
            'title': 'イベントの件名', 
            'start': datetime.datetime(), 
            'end': datetime.datetime(),
            'isAllDay': False, 
            'location': '場所の名前', 
            'id': 'title + start + end'

    Raises:
        Exception: カレンダーからイベント情報を取得できなかった場合に発生する例外。
    """

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calenderIds = ss.calenderIds
    gapi_creds = google.auth.load_credentials_from_file(
        os.path.join(ss.srcdir, ss.gcaljson), SCOPES)[0]
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

    if ss.debug:
        dtnow = ss.dtnow.isoformat() + 'Z'
        # dtnow = datetime.datetime(2023,3,8,11).isoformat() + 'Z'
    else:
        dtnow = datetime.datetime.utcnow().isoformat() + 'Z'
        
    events = []

    for calId in calenderIds:
        eventlist = service.events().list(
            calendarId = calId,
            timeMin = dtnow,
            maxResults = 5,
            singleEvents = True,
            orderBy = 'startTime'
        ).execute()

        if ss.debug:
            print(json.dumps(eventlist, ensure_ascii=False, indent=4))

        el = getRequiredData(eventlist, calId)
        events.extend(el)

    # events = sorted(events, key=lambda x: x['start'])

    # Remove events shared with calenderes
    uniqFlag = []
    uniqEvents = []
    for e in events:
        i = e['id']
        if i not in uniqFlag:
            uniqFlag.append(i)
            uniqEvents.append(e)
        else:
            for u in uniqEvents:
                if u['id'] == i:
                    u['calendar'] = 'Family'

    uniqEvents = sorted(uniqEvents, key=lambda x: x['start'])

    return uniqEvents

def drawV1(dr_imgBlk, dr_imgRed):
    events = getEvents()

    # 来客モード Visitor mode
    visitormode = ss.visitormode

    jst = pytz.timezone('Asia/Tokyo')
    if ss.debug:
        dn = jst.localize(ss.dtnow)
    else:
        dn = datetime.datetime.now()
        dn = jst.localize(dn)

    for _e in events:
        title = _e['title']
        if title.startswith('来客'):
            start = _e['start']
            end = _e['end']
            if start <= dn <= end:
                visitormode = True

    for i in range(3):
        if len(events) <= i:
            continue

        e = events[i]
        px = ss.margin + ss.colWid * i
        py = 390

        start = e['start']
        end = e['end']
        title = ss.limitTextLength(e['title'], 15)
        location = ss.limitTextLength(e['location'], 15)

        if visitormode:
            title = title[0] + "******"
            location = "*****"
            
        dateStr = [start.day, start.strftime('%a'), e['calendar'][:2]]
        timeStr = ''
        if e['isAllDay']:
            timeStr = '終日'
            
        elif start.date() == end.date():
            timeStr = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
        else:
            timeStr = f"{start.strftime('%H:%M')} - {end.strftime('%-m/%-d %H:%M')}"

        dr_imgBlk.rounded_rectangle((px-5, py-5, px+0.95*ss.colWid, py+110),
            outline=0, width=2, radius=8)
        for n, s in enumerate(dateStr):
            ss.textCenter(dr_imgBlk, (px + 20 , py + 15 + 30*n), str(s), 0, ss.fontBS)
        dr_imgBlk.text((px + 50, py), timeStr, 0, ss.fontNS)
        dr_imgBlk.text((px + 50, py + 30), title, 0, ss.fontNS)
        if location != '':
            dr_imgBlk.text((px + 50, py + 60), location, 0, ss.fontNS)

    return dr_imgBlk, dr_imgRed

def draw(dr_imgBlk, dr_imgRed):
    events = getEvents()
    
    # 来客モード Visitor mode
    visitormode = ss.visitormode

    jst = pytz.timezone('Asia/Tokyo')
    if ss.debug:
        dn = jst.localize(ss.dtnow)
    else:
        dn = datetime.datetime.now()
        dn = jst.localize(dn)

    for _e in events:
        title = _e['title']
        if title.startswith('来客'):
            start = _e['start']
            end = _e['end']
            if start <= dn <= end:
                visitormode = True


    dateStrPrev = ''
    isSameDate = False
    dispNum = 5 if not visitormode else 3

    for i in range(dispNum):
        if len(events) <= i:
            continue

        # 描画初期位置
        e = events[i]
        px = 250
        py = ss.margin + 75 * i

        # １イベントデータ
        dateStr = e['start'].strftime('%-d')
        dowStr = e['start'].strftime('%a')
        calname = e['calendar'][:2].capitalize()
        start = e['start']
        end = e['end']
        titleStr = ss.limitTextLength(e['title'], 30)
        locationStr = ss.limitTextLength(e['location'], 30)

        # １イベントデータ調整
        if visitormode:
            titleStr = titleStr[0] + " *" * len(titleStr)
            locationStr = " *" * len(locationStr)

        if start.day == ss.dtnow.day:
            dateStr = e['start'].strftime('今日')
        elif start.day == ss.dtnow.day + 1:
            dateStr = e['start'].strftime('明日')

        if dateStr == dateStrPrev:
            isSameDate = True
            
        timeStr = ''
        if e['isAllDay']:
            timeStr = '終日'
        elif start.date() == end.date():
            timeStr = f"{start.strftime('%H:%M')}\n{end.strftime('%H:%M')}"
        else:
            timeStr = f"{start.strftime('%H:%M')}\n{end.strftime('%-m/%-d %-H:%M')}"

        evntStr = titleStr + "\n" + locationStr

        # 描画
        # Col 1
        if not isSameDate:
            if start.day == ss.dtnow.day:
                dr_imgRed.text((290, py), dateStr, 0, ss.fontBS, align='center', anchor="ma")
                dr_imgRed.text((290, py + 30), dowStr, 0, ss.fontNS, align='center', anchor="ma")
            else:
                dr_imgBlk.text((290, py), dateStr, 0, ss.fontBS, align='center', anchor="ma")
                dr_imgBlk.text((290, py + 30), dowStr, 0, ss.fontNS, align='center', anchor="ma")

        dr_imgBlk.text((330, py), timeStr, 0, ss.fontNS)
        dr_imgBlk.text((410, py), calname, 0, ss.fontNS)
        dr_imgBlk.text((460, py), evntStr, 0, ss.fontNS)

        if not isSameDate:
            dr_imgBlk.line(((260, py-5), (840, py-5)), 0, 1)
        else:
            dr_imgBlk.line(((320, py-5), (840, py-5)), 0, 1)

        dateStrPrev = dateStr
        isSameDate = False
    
    lastLineY = ss.margin + 75 * dispNum - 5
    dr_imgBlk.line(((260, lastLineY), (840, lastLineY)), 0, 1)

    return dr_imgBlk, dr_imgRed


if __name__ == "__main__":
    events = getEvents()

    for e in events:
        print(e['calendar'], e['title'])