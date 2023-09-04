import os, datetime, locale, json
import setting as ss
import raspifuncs

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
    # dttmr = dtnow + datetime.timedelta(days=1)

    if ss.debug:
        dtnow = ss.dtnow
        # dttmr = dtnow + datetime.timedelta(days=1)
    
    holidayName = getHolidayName(dtnow)
    isWeekday = True
    if holidayName or dtnow.weekday() > 4:
        isWeekday = False

    centerX = 130
    dr_imgBlk.text((centerX, ss.margin), dtnow.strftime('%Y年 %-m月'), font=ss.fontNM, full=0, align="center", anchor="mt")

    if isWeekday:
        dr_imgBlk.text((centerX, 70), str(dtnow.day), 0, ss.fontBLL, align="center", anchor="mt")
        dr_imgBlk.text((centerX, 195), dtnow.strftime('%A'), 0, ss.fontBM, align="center", anchor="mt")
    else:
        dr_imgRed.text((centerX, 70), str(dtnow.day), 0, ss.fontBLL, align="center", anchor="mt")
        dr_imgRed.text((centerX, 195), dtnow.strftime('%A'), 0, ss.fontBM, align="center", anchor="mt")
        if holidayName:
            dr_imgRed.text((centerX, 230), holidayName, 0, ss.fontBS, align="center", anchor="ma")

    footnotes = 'LAST UPDATE: ' + dtnow.strftime('%Y-%m-%d %H:%M:%S')
    temp = raspifuncs.getCpuTemp()
    if (temp > 60):
        tempstr = f'■ {str(temp)} ℃ ■'
    else:
        tempstr = str(temp) + ' ℃'
    footnotes = footnotes + ' / CPU: ' + tempstr
    dr_imgRed.text((10, 512), footnotes, 0, ss.fontNSS)

    return dr_imgBlk, dr_imgRed


if __name__ == '__main__':
    print(getHolidayName(datetime.datetime(2023,5,2,12)))