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
                'location': loc
        }
        events.append(d)

    return events


def getEvents():
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

    events = sorted(events, key=lambda x: x['start'])
    return events

def draw(dr_imgBlk, dr_imgRed):
    events = getEvents()

    # 来客モード Visitor mode
    visitormode = ss.visitormode

    jst = pytz.timezone('Asia/Tokyo')
    dn = jst.localize(ss.dtnow)

    for _e in events:
        title = _e['title']
        if title.startswith('来客'):
            start = _e['start']
            end = _e['end']
            if start <= dn <= end:
                visitormode = True

    for i in range(3):
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

if __name__ == "__main__":
    getEvents()