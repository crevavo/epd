import os, sys, datetime, unicodedata
from PIL import ImageFont


# - Func setting -----
debug = True
dtnow = datetime.datetime.now()
visitormode = False


# - Project setting -----
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
srcdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'src')
if os.path.exists(libdir):
    sys.path.append(libdir)

fontBLL = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Bold.ttf'), 140)
fontBL = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Bold.ttf'), 48)
fontBM = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Bold.ttf'), 28)
fontBS = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Bold.ttf'), 22)
fontNL = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Normal.ttf'), 48)
fontNM = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Normal.ttf'), 28)
fontNS = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Normal.ttf'), 24)
fontNSS = ImageFont.truetype(os.path.join(picdir, 'GenShinGothic-Normal.ttf'), 12)
fontWIL = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 68)
fontWIS = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 42)

epdWid = 880
epdHei = 528
margin = 20
colWid = (int)(epdWid - margin * 2) / 3

# - Open Weather setting -----
LAT = 35.6896342
LON = 139.6921007
OWM_KEY = 'API Key for OpenWeatherMap One Call API'

# - Gargage Calender setting -----
# DayOfWeek ==> 0: Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri, 5:Sat, 6:Sun
# [DayOfWeek, DayOfWeek, ...]
# [(Nth, DayOfWeek), (Nth, DayOfWeek), ...]
gcDict = {
        'もえるゴミ': [0, 3],
        'もえないゴミ': [(1,2), (3, 2)],
        '資源回収': [(2,3), (4,3)],
    }

# - Google Calender setting -----
calenderIds = ['alice@gmail.com', 'bob@gmail.com']
gcaljson = 'googlecalender.json'

# - Train info setting -----
trainUrl = "https://transit.yahoo.co.jp/diainfo/21/0"

# - Utility functions -----
def limitTextLength(text, len):
    # 全角・半角を区別して文字列を切り詰める
    count = 0
    sliced_text = ''
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1

        # lenと同じ長さになったときに抽出完了
        if count > len:
            sliced_text += '...'
            break
        sliced_text += c
    return sliced_text

def textCenter(draw, pos, message, fontColor, font):
    x, y = pos
    _, _, w, h = draw.textbbox((0,0), message, font=font)
    tx, ty = (int(x - w/2), int(y - h/2))
    draw.text((tx,ty), message, font=font, fill=fontColor)