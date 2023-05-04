import os, datetime, locale, json
import setting as ss

# --- Date display ------------------
def getHolidayName(dt = datetime.datetime.now() ):

    jsonpath = os.path.join(ss.srcdir, 'holidays.json')
    with open(jsonpath) as f:
        holidays = json.load(f)
    
    dtstr = dt.strftime('%Y-%m-%d')
    
    if dtstr in holidays:
        return holidays[dtstr]
    
    return None


def draw(dr_imgBlk, dr_imgRed):
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

    dtnow = datetime.datetime.now()
    dttmr = dtnow + datetime.timedelta(days=1)

    if ss.debug:
        dtnow = ss.dtnow
        dttmr = dtnow + datetime.timedelta(days=1)
    
    holidayName = getHolidayName(dtnow)

    dr_imgBlk.text((ss.margin, 5), dtnow.strftime('%Y-%m'), font = ss.fontNL, fill = 0)

    if holidayName:
        dr_imgRed.text((220, 15), holidayName, 0, ss.fontNM)

    ss.textCenter(dr_imgBlk, (100, 125), str(dtnow.day), 0, ss.fontBLL)
    dr_imgRed.text((ss.margin + 170, 110), dtnow.strftime('%a'), 0, ss.fontBL)

    dtFormat = '%-m / %-d (%a)'
    # dr_imgBlk.text((s.margin + colWid*0, s.margin), dtnow.strftime(dtFormat), font = s.fontBL, fill = 0)
    # dr_imgBlk.text((s.margin + colWid*2, s.margin), dttmr.strftime(dtFormat), font = s.fontBL, fill = 0)
    dr_imgRed.text((0, 512), 'LAST UPDATE: ' + dtnow.isoformat(), 0, ss.fontNSS)

    return dr_imgBlk, dr_imgRed


if __name__ == '__main__':
    print(getHolidayName(datetime.datetime(2023,5,2,12)))