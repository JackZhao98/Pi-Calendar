import sys
sys.path.append('/home/jackzhao/env/lib')
from waveshare_epd import epd2in7
from Pi_Calendar import PiCalendarDelegate
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import calendar

'''
EPD_WIDTH       = 176
EPD_HEIGHT      = 264
'''

def fetch_data(url = "", number = 5):
    pcd = PiCalendarDelegate()
    event_list = pcd.fetch_events(url)
    return pcd.sanitize(event_list, number)

def generate_pic(event_list):
    tzinfo = timezone(timedelta(hours = -7))
    light_font = "/home/jackzhao/Developer/CalendarPi/assets/Light.ttf"
    mid_font = "/home/jackzhao/Developer/CalendarPi/assets/Medium.ttf"
    bold_font  = "/home/jackzhao/Developer/CalendarPi/assets/Bold.ttf"
    background = Image.open('/home/jackzhao/Developer/CalendarPi/assets/pic.png')

    epd = epd2in7.EPD()
    buffer_img = Image.new('1', (epd.height, epd.width), 255)
    ttf10_light = ImageFont.truetype(light_font, 10)
    ttf10_mid = ImageFont.truetype(mid_font, 10)
    ttf10_bold = ImageFont.truetype(bold_font, 10)
    ttf12_bold = ImageFont.truetype(bold_font, 13)
    ttf15_bold = ImageFont.truetype(bold_font, 15)
    ttf25_light = ImageFont.truetype(light_font, 25)
    ttf32_bold = ImageFont.truetype(bold_font, 32)

    draw = ImageDraw.Draw(buffer_img)

    calendar_x, calendar_y = 10, 6
    today = datetime.now()
    Day = today.astimezone(tzinfo).strftime("%A")
    Date = today.astimezone(tzinfo).strftime("%b %d")
    week = int(today.astimezone(tzinfo).strftime("%U")) - 39

    draw.text((calendar_x, calendar_y),  Date, font=ttf32_bold, fill=0)
    draw.text((calendar_x, calendar_y + 30), Day, font=ttf25_light, fill=0)
    draw.text((calendar_x, calendar_y + 65), f"Week {week}", font=ttf15_bold, fill=0)
    buffer_img.paste(background, (34, 100))

    event_x, event_y = 140, 6

    for e in event_list:
        summary = e['summary']
        start = e['datestart'].astimezone(tzinfo).strftime("%b %d %H:%M")
    
        draw.text((event_x, event_y), summary, font=ttf12_bold, fill=0)

        start_w, start_h = ttf10_mid.getsize(start)

        draw.text((epd.height - 10 - start_w, event_y + 15), start, font=ttf10_mid, fill=0)
        event_y += 29

        #  event_x + 40
        draw.line((event_x + 40, event_y, epd.height, event_y), fill = 0)
        event_y += 5


    
    message = "Last run: " + today.astimezone(tzinfo).strftime("%H:%M") + "."
    draw.text((6, epd.width - 13), message, font=ttf10_mid, fill=0)
    return buffer_img

def render(buffer_img):
    epd = epd2in7.EPD()
    epd.init()
    epd.display(epd.getbuffer(buffer_img))

class PiCalendar():
    """docstring for PiCalendar"""
    def __init__(self, url):
        self.url = url
    def update(self):
        event_list = fetch_data(self.url, 5)
        frame = generate_pic(event_list)
        render(frame) 
        

