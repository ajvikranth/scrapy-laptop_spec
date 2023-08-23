import scrapy
import sqlite3
from ..items import LaptopSpecScraperItem

class ProductDescSpider(scrapy.Spider):

    name = 'ProductDesc'
    base_url = 'https://www.flipkart.com'
    pnum = 0

    # Constants and Configuration
    DB_FILE = "product.db"
    TABLE_NAME = "productlink"

    custom_settings = {
        'ITEM_PIPELINES': {
            "laptop_spec_scraper.pipelines.ProductDescScraperPipeline": 300,
        }
    }

    def start_requests(self):
        # Connect to the database
        self.conn = sqlite3.connect(self.DB_FILE)
        self.cur = self.conn.cursor()

        # Fetch all rows from the productlink table
        self.cur.execute(f"SELECT * FROM {self.TABLE_NAME}")
        self.rows = self.cur.fetchall()
        self.rows_c = len(self.rows)

        # Build the URL for the first request
        url = self.base_url + self.rows[self.pnum][2]
        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        item = LaptopSpecScraperItem()
        
        # Extract basic item information
        item["pnum"] = self.rows[self.pnum][0]
        item["brand"] = response.css(".B_NuCI::text").get(default='NULL')
        item['price'] = response.css("._16Jk6d::text").get(default='NULL')
        item['discount'] = response.css("._31Dcoz span::text").get(default='NULL')
        item['rating'] = response.css("._2d4LTz::text").get(default='NULL')
        rat_rev_n = response.css("._2afbiS span::text").extract()

        # Extract and process ratings and reviews data
        if rat_rev_n !=[]:
            item['n_ratings'] = int(rat_rev_n[0].split(" ")[0].replace(",",""))
            item['n_reviews'] = int(rat_rev_n[1].split(" ")[0].replace(",",""))
        else:
            item['n_ratings'] = 'NULL'
            item['n_reviews'] = 'NULL'


        # Extract specific laptop specifications
        for desc , val in zip(response.css('td._1hKmbr.col.col-3-12::text').extract(),response.css('li._21lJbe::text').extract()):

            if desc in ['Model Number','Type','Suitable For','Processor Brand','Processor Name','SSD Capacity','RAM','Graphic Processor','Operating System','Screen Size','Screen Resolution','HDD Capacity']:
                desc = desc.replace(" ","_")
                item[desc]=val

        # Yield the item to the pipeline for further processing
        yield item
        self.pnum+=1
        
        # Check if there are more pages to scrape
        if  self.pnum <self.rows_c  : # 
            next_page = self.base_url + self.rows[self.pnum][2]
            yield response.follow(next_page, callback=self.parse)
