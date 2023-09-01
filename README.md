# E-Ink Paper Display - Personal calendar
![epd-banner-gh](https://github.com/crevavo/epd/assets/10239961/ffbc511f-9a6e-4f51-9a14-cd04cf18aa39)

Source codes for E-Ink display personal calendar project.

## Features
Display following data to E-Ink Paper display with Raspberry Pi.

- Date display
- Japan, Garbage collection calendar
- Weather Info (Today/Tomorrow/3 hours)
- Google Calendar events

## Requirements
**Hard ware**
- Raspberry Pi
- E-Ink Display

**Software**
- This codes
- OpenWeatherMap API settings
- Google Calendar API settings

## Setup
### API keys setting
Need to get API keys for OpenWheatherMap (OWM) and Google Calendar.

OWM provides Key strings. Google Calendar provides credential JSON file.

### Update setting files
Use venv for install python packages
```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Put setting file
```bash
cp src/setting.default.py src/setting.py
vi src/setting.py
```
and update following settings

```
# - Open Weather setting -----
LAT = 35.6896342
LON = 139.6921007
OWM_KEY = 'API Key for OpenWeatherMap One Call API'

# - Gargage Calender setting -----
# DayOfWeek ==> 0: Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri, 5:Sat, 6:Sun
# [DayOfWeek, DayOfWeek, ...]
# [(Nth, DayOfWeek), (Nth, DayOfWeek), ...]
gcDict = { }

# - Google Calender setting -----
calenderIds = ['alice@gmail.com', 'bob@gmail.com']
gcaljson = 'googlecalender.json'
```

Set path to Google Calender credential json file to gcaljson setting.

## Run
For check render image, just run
```bash
python ~/epd/src/epd-cal-img.py
```
Script export .bmp file to project root. You can check it by image viewer.


To use with E-Ink Display and Raspberry Pi, setup cron.
```bash:cron
python ~/epd/src/epd-calendar.py
```
Script display image to EPD.

## Site
https://hyogo.dev/works/epd
