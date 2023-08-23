import scrapy
import sqlite3
import js2xml
import lxml.etree
from parsel import Selector
from ..items import LaptopSpecScraperItem


class ProductReviewSpider(scrapy.Spider):

    name = 'ProductReview'
    base_url = 'https://www.flipkart.com'
    pnum = 0
    review_count = 0
    page_count = 1

    custom_settings = {
        'ITEM_PIPELINES': {
            "laptop_spec_scraper.pipelines.ProductReviewScraperPipeline": 300,
        }
    }
  

    def start_requests(self):
        # Connect to the database
        self.conn = sqlite3.connect("product.db")
        self.cur = self.conn.cursor()

        # Fetch all rows from the productlink table
        self.cur.execute("SELECT * FROM productlink")
        self.rows = self.cur.fetchall()
        self.rows_c = len(self.rows)
        
        # Build the URL for the first request
        url = self.base_url + self.rows[self.pnum][2].replace("/p/","/product-reviews/") + "&page="+ str(self.page_count)

        
        yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        # Fetch the review count from the database
        self.conn = sqlite3.connect("product.db")
        self.cur = self.conn.cursor()
        query = "select n_reviews from productdesc where pnum=" + str(self.rows[self.pnum][0])
        self.cur.execute(query)
        self.review_count = self.cur.fetchall()[0][0] 

        if self.review_count == 'NULL':
            # No reviews available for this product, move to the next product
            self.pnum+=1
            self.page_count=1
            next_page = self.base_url + self.rows[self.pnum][2].replace("/p/","/product-reviews/") + "&page="+ str(self.page_count)
            
            yield scrapy.Request(url=next_page, callback=self.parse)

        elif  self.pnum < self.rows_c-1 and response.css("._2-N8zT::text").extract() ==[]:
            # Move to the next product if no reviews found for the current one
            ProductReviewSpider.pnum+=1
            ProductReviewSpider.page_count=1
            next_page = ProductReviewSpider.base_url + self.rows[ProductReviewSpider.pnum][2].replace("/p/","/product-reviews/")  + "&page="+ str(ProductReviewSpider.page_count)
             
            yield scrapy.Request(url=next_page, callback=self.parse)       

        elif  response.css("._2-N8zT::text").extract() !=[]:

            item = LaptopSpecScraperItem()
     
            pnum = self.rows[self.pnum][0]
            review_titles = response.css("._2-N8zT::text").getall()
            review_rating = response.css("._1BLPMq::text").getall() 
            review_date = response.css("div+ ._2sc7ZR::text").getall() 
            loc_html = response.css("._2mcZGG").getall()
            review = [] 
            location =[]
            
            for html in loc_html:
                selector = Selector(text=html)
                loc = selector.css('span::text').getall()

                if len(loc)==2:
                    loc = loc[1]
                    location.append(loc)
                else:
                    location.append(None) 
  
            jss = response.css("script::text").getall()[8]

            xml = lxml.etree.tostring(js2xml.parse(jss), encoding="unicode")
            selector = Selector(text=xml)
            res= selector.xpath('//property[@name="text"]').getall()[2:-6]
            
            for r in res:
                selector = Selector(text=r)
                a=selector.xpath('//string/text()').get()
                
                review.append(a)

            if len(location) != len(review):

                    location = (len(review) -len(location))*['NULL']
                
            for i in range(len(review)):   
            
                item['pnum'] = pnum
                item['review_title'] =review_titles[i]
                item['review_rating'] =review_rating[i]
                item['review_date'] =review_date[i]
                item['review'] =review[i]
                item['location']  = location[i]

                yield item

                
            self.page_count+=1
            next_page = self.base_url + self.rows[self.pnum][2].replace("/p/","/product-reviews/") + "&page="+ str(self.page_count)
            
            yield scrapy.Request(url=next_page, callback=self.parse)

       