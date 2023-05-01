import datetime, locale
import setting as ss

# --- Date display ------------------
def draw(dr_imgBlk, dr_imgRed):
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

    dtnow = datetime.datetime.now()
    dttmr = dtnow + datetime.timedelta(days=1)

    if ss.debug:
        dtnow = ss.dtnow
        dttmr = dtnow + datetime.timedelta(days=1)

    dr_imgBlk.text((ss.margin, 5), dtnow.strftime('%Y-%m'), font = ss.fontNL, fill = 0)
    dr_imgBlk.text((ss.margin, 80), str(dtnow.day), 0, ss.fontBLL)

    dr_imgRed.text((ss.margin + 140, 110), dtnow.strftime('%a'), 0, ss.fontBL)

    dtFormat = '%-m / %-d (%a)'
    # dr_imgBlk.text((s.margin + colWid*0, s.margin), dtnow.strftime(dtFormat), font = s.fontBL, fill = 0)
    # dr_imgBlk.text((s.margin + colWid*2, s.margin), dttmr.strftime(dtFormat), font = s.fontBL, fill = 0)
    dr_imgRed.text((0, 512), 'LAST UPDATE: ' + dtnow.isoformat(), 0, ss.fontNSS)

    return dr_imgBlk, dr_imgRed
