# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join
from datetime import datetime


def get_id(text):
    # Strip "№ "
    return text[2:]


def remove_spaces(text):
    # Remove spaces
    return text.replace(" ", "")


def area(text):
    # Initial: Площадь: 51 м² (жилая: 35 м², кухня: 9 м²)
    return text.split()[1]


def room(text):
    # Initial: Площадь: 51 м² (жилая: 35 м², кухня: 9 м²)
    return text.split()[0]


def floor(arr):
    # Initial: Этаж 4\5
    return arr.split()[1].split('/')[0]


def added(text):
    #["Добавлено 28.09, обновлено ", "Объявление просматривали 242 раза, 
    # интересовались контактами 12 раз."]
    return text.split()[1][:-1]


def convert_date(date):
    # convert string March 14, 1879 to Python date
    return datetime.strptime(date+' 2021', '%d.%m %Y')


def url_photos(text):
    url = text[44:-9]
    return url.replace("/s/", "/l/")


class SakhcomItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ad_id = Field(
        output_processor=TakeFirst())
    price = Field(
        input_processor=MapCompose(remove_spaces),
        output_processor=TakeFirst())
    area = Field(
        input_processor=MapCompose(area),
        output_processor=TakeFirst())
    floor = Field(
        input_processor=MapCompose(floor),
        output_processor=Join())
    room = Field(
        input_processor=MapCompose(room),
        output_processor=TakeFirst())
    address = Field(
        output_processor=Join())
    params = Field()
    added = Field(
        input_processor=MapCompose(added),
        output_processor=TakeFirst())
    updated = Field(
        output_processor=TakeFirst())
    photo_inside = Field(
        input_processor=MapCompose(url_photos))
    photo_outside = Field()
    url = Field()
    pass
