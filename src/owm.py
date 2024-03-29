import os, requests, json, datetime

import setting as ss

# --- Wheather Forecast ------------------
# Src: https://openweathermap.org/
# Icon: https://erikflowers.github.io/weather-icons/

def getWheatherIconUnicode(owmid, dt = datetime.datetime.now()):
    with open(os.path.join(ss.srcdir, 'wheather-icons.json')) as f:
        iconTable = json.load(f)

    daynight = 'all'
    if 6 <= dt.hour < 18:
        daynight = 'day'
    else:
        daynight = 'night'
    
    if daynight in iconTable[str(owmid)]:
        return int(iconTable[str(owmid)][daynight]['font'], 16)
    
    return int(iconTable[str(owmid)]['all']['font'], 16)

def getOWMdata():
    lat, lon, owmkey = ss.LAT, ss.LON, ss.OWM_KEY
    owmapi = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={apikey}&units=metric'
    url = owmapi.format(lat = lat, lon = lon, apikey = owmkey)

    if ss.debug:
        print('**** Weather setting ****')
        print('Load URL: ' + url)
        print('This time, use dummy data for OWM data')
        # Dummy data
        with open(os.path.join(ss.srcdir, 'owm.json')) as f:
            d = json.load(f)
    else:
        r = requests.get(url)
        d = r.json()
        # print(json.dumps(d, indent=4))
    return d

def draw(dr_imgBlk, dr_imgRed, d):

    centerY = 455

    # ---- Display TODAY
    wtoday = d['daily'][0]
    owmdt = datetime.datetime.fromtimestamp(wtoday['dt'])
    owmid = wtoday['weather'][0]['id']
    wicon = getWheatherIconUnicode(owmid, owmdt)
    if owmid >= 800:
        dr_imgRed.text((90, centerY), chr(wicon), 0, ss.fontWIL, align="center", anchor="mm")
    else:
        dr_imgBlk.text((90, centerY), chr(wicon), 0, ss.fontWIL, align="center", anchor="mm")

    tempStr = f"{wtoday['temp']['max']:.0f} ℃\n{wtoday['temp']['min']:.0f} ℃"
    dr_imgBlk.text((170, centerY), tempStr, 0, ss.fontNM, align="right", anchor="lm")

    # ---- Display Tomorrow forecast
    # wtomorrow = d['daily'][1]
    # owmdt = datetime.datetime.fromtimestamp(wtomorrow['dt'])
    # owmid = wtomorrow['weather'][0]['id']
    # wicon = getWheatherIconUnicode(owmid, owmdt)

    # if owmid >= 800:
    #     dr_imgRed.text((ss.margin*1 + ss.colWid*2, 100), chr(wicon), 0, ss.fontWIL)
    # else:
    #     dr_imgBlk.text((ss.margin*1 + ss.colWid*2, 100), chr(wicon), 0, ss.fontWIL)

    # tempStr = f"{wtomorrow['temp']['max']:.0f} ℃\n{wtomorrow['temp']['min']:.0f} ℃"
    # dr_imgBlk.text((ss.margin*2 + ss.colWid*2 + 120, 110), tempStr, 0, ss.fontNM)

    # ---- Display 3 Hours forecast
    
    xstr = 270
    xend = 840
    lcolWid = (xend - xstr) / 5
    lcolOffset = lcolWid / 2

    for i in range(5):
        whour = d['hourly'][i*3]
        owmdt = datetime.datetime.fromtimestamp(whour['dt'])
        owmid = whour['weather'][0]['id']
        wicon = getWheatherIconUnicode(owmid, owmdt)
        hourStr = owmdt.strftime('%-H:%M')
        tempStr = f"{whour['temp']:.0f} ℃"

        px = xstr + lcolOffset + lcolWid * i
        pyUpper = centerY - 30
        pyLower = centerY + 20

        if 6 <= owmdt.hour <= 18:
            dr_imgBlk.text((px, pyUpper), hourStr, 0, ss.fontBS, align="center", anchor="mm")
        else:
            dr_imgBlk.text((px, pyUpper), hourStr, 0, ss.fontNS, align="center", anchor="mm")

        if owmid >= 800:
            dr_imgRed.text((px, pyLower), chr(wicon), 0, ss.fontWIS, align="center", anchor="mm")
            # ss.textCenter(dr_imgRed, (px + lcolWid/2, py+50), chr(wicon), 0, ss.fontWIS)
        else:
            dr_imgBlk.text((px, pyLower), chr(wicon), 0, ss.fontWIS, align="center", anchor="mm")
            # ss.textCenter(dr_imgBlk, (px + lcolWid/2, py+50), chr(wicon), 0, ss.fontWIS)
        
        # ss.textCenter(dr_imgBlk, (px + lcolWid/2, py+100), tempStr, 0, ss.fontNS)

    return dr_imgBlk, dr_imgRed

if __name__ == "__main__":
    data = getOWMdata()

    print(json.dumps(data, indent=4))
    with open('owm.json', 'w') as f:
        json.dump(data, f, indent=4)
