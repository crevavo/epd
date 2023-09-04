#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os, logging, traceback, time
from PIL import Image,ImageDraw,ImageChops

import setting as ss
import owm, datedisp, garbagecal, googlecal, train
picdir, libdir, srcdir = ss.picdir, ss.libdir, ss.srcdir
logging.basicConfig(level=logging.DEBUG)

from waveshare_epd import epd7in5b_HD

try:
    epd = epd7in5b_HD.EPD()

    logging.info("Drawing ...")

    imgBlk = Image.new('1', (ss.epdWid, ss.epdHei), 255)
    imgRed = Image.new('1', (ss.epdWid, ss.epdHei), 255)
    dr_imgBlk = ImageDraw.Draw(imgBlk)
    dr_imgRed = ImageDraw.Draw(imgRed)

    # --- Date display ------------------
    dr_imgBlk, dr_imgRed = datedisp.draw(dr_imgBlk, dr_imgRed)

    # --- Weather Info ------------------
    owmdata = owm.getOWMdata()
    dr_imgBlk, dr_imgRed = owm.draw(dr_imgBlk, dr_imgRed, owmdata)

    # --- Garbage Info ------------------
    dr_imgBlk, dr_imgRed = garbagecal.draw(dr_imgBlk, dr_imgRed)

    # --- Google Calender ------------------
    dr_imgBlk, dr_imgRed = googlecal.draw(dr_imgBlk, dr_imgRed)

    # --- Train info ------------------
    if ss.visitormode:
        dr_imgBlk, dr_imgRed = train.draw(dr_imgBlk, dr_imgRed)

    # - Wi-Fi QR code ---------------------
    if ss.visitormode:
        qrcode = Image.open(os.path.join(picdir, 'wifi.bmp'))
        imgBlk.paste(qrcode, (700, 250))


    # - DEBUG img export ----------
    imgRGB = Image.new('RGB', (ss.epdWid, ss.epdHei), (255, 255, 255))

    imgBlkInv = ImageChops.invert(imgBlk)
    imgRedInv = ImageChops.invert(imgRed)
    imgRGB.paste(Image.new('RGB', (ss.epdWid, ss.epdHei), (0, 0, 0)), (0, 0), imgBlkInv)
    imgRGB.paste(Image.new('RGB', (ss.epdWid, ss.epdHei), (230, 0, 51)), (0, 0), imgRedInv)
    
    imgRGB.save('img.bmp')

    # - Display Update ----------
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    epd.display(epd.getbuffer(imgBlk),epd.getbuffer(imgRed))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_HD.epdconfig.module_exit()
    exit()
