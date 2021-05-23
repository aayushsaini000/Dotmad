# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DotmadItem(scrapy.Item):
    Line = scrapy.Field()
    ListingTitle = scrapy.Field()
    ListingNumber = scrapy.Field()
    ListingLink = scrapy.Field()
    AskingPrice = scrapy.Field()
    Condition = scrapy.Field()
    QtyAvailable = scrapy.Field()
    InStock = scrapy.Field()
    Date = scrapy.Field()
    Company = scrapy.Field()
    RepName = scrapy.Field()
    RepLink = scrapy.Field()
    Reviews = scrapy.Field()
    Location = scrapy.Field()
    Phone = scrapy.Field()
    Brand = scrapy.Field()
    Type = scrapy.Field()
    Model = scrapy.Field()
    Category = scrapy.Field()
    SubCategory = scrapy.Field()
    Description = scrapy.Field()
    pass
