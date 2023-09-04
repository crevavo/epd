import datetime
import setting as ss

def draw(dr_imgBlk, dr_imgRed):
    gcDict = ss.gcDict
    dtnow = datetime.datetime.now()
    if ss.debug:
        dtnow = ss.dtnow

    if dtnow.hour <= 10:
        gdt = dtnow
        gdatelabel = '《 きょう朝 》\n'
    else:
        gdt = dtnow + datetime.timedelta(days=1)
        gdatelabel = '（ あす朝 ）\n'

    dow = gdt.weekday()
    nth = (gdt.day - 1) // 7 + 1

    glabel = []

    for k, v in gcDict.items():
        for i in v:
            if isinstance(i, tuple):  # check as Nth/DayOfWeek
                if i[0] == nth and i[1] == dow:
                    glabel.append(k)
            else: # check as DayOfWeek
                if i == dow:
                    glabel.append(k)

    if len(glabel) <= 0:
        glabel.append('回収なし')

    py = 290
    centerX = 130

    gstr = gdatelabel + '\n'.join(glabel)
    dr_imgBlk.text((centerX, py), gstr, 0, ss.fontNS, align="center", anchor="ma")

    return dr_imgBlk, dr_imgRed