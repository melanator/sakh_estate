# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join
from datetime import datetime, timedelta


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
    """
    Retrieve date from "Добавлено 28.09, обновлено. Объявление просматривали 242 раза, интересовались контактами 12 раз." string
    """
    return text.split()[1][:-1]


def convert_date(date):
    """
    Gets date string as in input and return datetime.date() object
    """
    if date == 'сегодня':
        return datetime.today().date()
    elif date == 'вчера':
        return (datetime.today() - timedelta(days=1)).date()
    # convert string March 14, 1879 to Python date
    if not any(char.isdigit() for char in date):
        return date
    if len(date.split('.')) == 2:
        date += '.2021'
    return datetime.strptime(date, '%d.%m.%Y').date()


def url_photos(text):
    url = text[44:-9]
    return url.replace("/s/", "/l/")


def to_int(text):
    return int(text)


def updated(text):
    if text == 'сегодня':
        return datetime.today().date()
    elif text == 'вчера':
        return (datetime.today() - timedelta(days=1)).date()
    try:
        # If data can be transfomed to datetime object
        return datetime.strptime(text, '%d.%m.%Y').date()
    except ValueError:
        num, text = text.split(' ', 1)
        if 'дн' in text:
            return (datetime.today() - timedelta(days=int(num))).date()
        if 'нед' in text:
            return (datetime.today() - timedelta(weeks=int(num))).date()
        if 'мес' in text:
            return (datetime.today() - timedelta(days=int(num)*30)).date()


class SakhcomItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ad_id = Field(
        output_processor=TakeFirst())
    price = Field(
        input_processor=MapCompose(remove_spaces, to_int),
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
        input_processor=MapCompose(added, convert_date),
        output_processor=TakeFirst())
    updated = Field(
        input_processor=MapCompose(updated),
        output_processor=TakeFirst())
    photo_inside = Field(
        input_processor=MapCompose(url_photos))
    photo_outside = Field()
    url = Field()
    scraped = Field(output_processor=TakeFirst())
