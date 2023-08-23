# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LaptopSpecScraperItem(scrapy.Item):
    # define the fields for your item here like: name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()

    pnum = scrapy.Field()
    price =scrapy.Field()
    discount =scrapy.Field()
    rating = scrapy.Field()
    n_ratings = scrapy.Field()
    n_reviews = scrapy.Field()
    
    brand =scrapy.Field()
    Model_Number= scrapy.Field()
    Type = scrapy.Field()
    Suitable_For = scrapy.Field()
    Processor_Brand = scrapy.Field()
    Processor_Name = scrapy.Field()
    SSD_Capacity = scrapy.Field()
    RAM = scrapy.Field()
    Graphic_Processor = scrapy.Field()
    Operating_System = scrapy.Field()
    Screen_Size  = scrapy.Field()
    Screen_Resolution = scrapy.Field()
    HDD_Capacity = scrapy.Field()


    review_title = scrapy.Field()
    review_rating = scrapy.Field()
    review_date = scrapy.Field()
    review = scrapy.Field()
    location = scrapy.Field()
                    
    
