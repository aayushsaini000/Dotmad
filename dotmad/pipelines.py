# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import requests
import csv
import os
import glob
import pytz
import time
import datetime
import logging as log
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from lxml.html import fromstring
from itertools import cycle
import sys

class DotmadPipeline:
    def __init__(self,filename):
        self.files = {}
        self.file_name = filename+".xlsx" #f'dotmed{time.time()}.xlsx'
        self.export_fields = [
            'Line', 'ListingTitle', 'ListingNumber', 'ListingLink', 'AskingPrice',
            'Condition', 'QtyAvailable', 'InStock', 'Date', 'Company', 'RepName', 'RepLink',
            'Reviews', 'Location', 'Phone', 'Brand', 'Type', 'Model',
            'Category','SubCategory']

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        filename = settings.get("filename")
        pipeline = cls(filename)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        output_file = open(
            self.file_name,
            'w+b',
        )
        self.files[spider] = output_file
        self.exporter = CsvItemExporter(
            output_file,
            fields_to_export=self.export_fields
        )
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        output_file = self.files.pop(spider)
        output_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


