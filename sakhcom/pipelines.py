# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter


class SakhcomPipeline:
    filename = 'sale.json'

    def __init__(self):
        self.file = open(self.filename, 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.indent = True
        self.exporter.start_exporting()
        pass

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class LeasePipeline(SakhcomPipeline):
    filename = 'lease.json'
