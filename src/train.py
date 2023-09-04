import requests
from bs4 import BeautifulSoup
import setting as ss

# --- Wheather Forecast ------------------
# Src: https://openweathermap.org/
# Icon: https://erikflowers.github.io/weather-icons/

# url = 'https://transit.yahoo.co.jp/diainfo/22/0'

def getTrainInfo(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.select_one("h1.title").text
    status = soup.select_one(".elmServiceStatus > dl > dt").text
    detail = soup.select_one(".elmServiceStatus > dl > dd").text

    isOk = True if status == "平常運転" else False

    d = {
        'title': title,
        'status': status,
        'detail': detail,
        'isOk': isOk
    }
    return d

def draw(dr_imgBlk, dr_imgRed):
    
    if ss.debug:
        dtnow = ss.dtnow
        # dttmr = dtnow + datetime.timedelta(days=1)

    d = getTrainInfo(ss.trainUrl)

    title = d['title']
    status = d['status']
    detail = d['detail']

    linewid = 17
    if len(detail) > linewid:
        if len(detail) > linewid*2:
            detail = detail[0:linewid] + '\n' + detail[linewid:linewid*2 -2] + "..."
        else:
            detail = detail[0:linewid] + '\n' + detail[linewid:linewid*2]

    dr_imgBlk.text((270, 250), title, 0, ss.fontNS, anchor="la")

    if d['isOk']:
        dr_imgBlk.text((270, 290), status, 0, ss.fontBS, anchor="la")
        dr_imgBlk.text((270, 320), detail, 0, ss.fontNS, anchor="la")
    else:
        dr_imgRed.text((270, 290), status, 0, ss.fontBS, anchor="la")
        dr_imgRed.text((270, 320), detail, 0, ss.fontNS, anchor="la")
    
    return dr_imgBlk, dr_imgRed
    

if __name__ == '__main__':
    d = getTrainInfo(ss.trainUrl)
    print(d)