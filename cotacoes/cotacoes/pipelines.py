# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import pymongo

class CotacoesPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.connection.close()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.update( { 'data' : item['data'] }, dict(item), upsert=True)
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item