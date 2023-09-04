import sys, os, logging, traceback
from PIL import Image,ImageDraw,ImageChops

import setting as ss
import owm, datedisp, garbagecal, googlecal
picdir, libdir, srcdir = ss.picdir, ss.libdir, ss.srcdir
logging.basicConfig(level=logging.DEBUG)

try:
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

    # - Wi-Fi QR code ---------------------
    # if ss.debug:
    #     qrcode = Image.open(os.path.join(picdir, 'qrcode.bmp'))
    # else:
    #     qrcode = Image.open(os.path.join(picdir, 'wifi.bmp'))
    # imgBlk.paste(qrcode, (ss.epdWid-100, 0))

    # - Post tasks ---------------------
    imgRGB = Image.new('RGB', (ss.epdWid, ss.epdHei), (255, 255, 255))

    imgBlkInv = ImageChops.invert(imgBlk)
    imgRedInv = ImageChops.invert(imgRed)
    imgRGB.paste(Image.new('RGB', (ss.epdWid, ss.epdHei), (0, 0, 0)), (0, 0), imgBlkInv)
    imgRGB.paste(Image.new('RGB', (ss.epdWid, ss.epdHei), (230, 0, 51)), (0, 0), imgRedInv)
    
    imgRGB.save('img.bmp')
    # imgBlk.save('imgB.bmp')
    # imgRed.save('imgR.bmp')
    

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
