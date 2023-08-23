# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class ProductLinkScraperPipeline:

    def __init__(self) :
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("product.db")
        self.corr = self.conn.cursor()

    def create_table(self):
        self.corr.execute('''DROP TABLE IF EXISTS PRODUCTLINK''')
        self.corr.execute('''CREATE TABLE ProductLink (pnum integer primary key, 
                                          title text,
                                          link text) ''')


    def process_item(self, item, spider):
        self.store_item(item)
        return item
    
    def store_item(self,item):
        self.corr.execute('''INSERT INTO PRODUCTLINK(title,link) VALUES (?,?)''',(item["title"],item["link"]))
        self.conn.commit()

class ProductDescScraperPipeline:

    def __init__(self) :
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("product.db")
        self.corr = self.conn.cursor()

    def create_table(self):
        self.corr.execute('''DROP TABLE IF EXISTS PRODUCTDESC''')
        self.corr.execute('''create table productdesc (  
            pid integer primary key,   
            pnum integer not null,   
            price integer,   
            discount integer,   
            rating real,   
            n_ratings integer,   
            n_reviews integer,   
            foreign key (pnum) references productlink (pnum)
            ); ''')
        
        self.corr.execute('''DROP TABLE IF EXISTS PRODUCTSPECS''')
        self.corr.execute('''
            create table productspecs (  
            pid integer primary key,   
            pnum integer not null,   
            brand text,
            Model_Number text,
            Type text,
            Suitable_For text,
            Processor_Brand text,
            Processor_Name text,
            SSD_Capacity_GB integer,
            HDD_Capacity_GB  integer,
            RAM_GB integer,
            Graphic_Processor text,
            Operating_System text,
            Screen_Size_cm real,  
            Screen_Resolution text,
            foreign key (pnum) references productlink (pnum)
            ); ''')


    def process_item(self, item, spider):
        self.store_item(item)
        return item
    
    def store_item(self,item):
        
        price = int(item["price"][1:].replace(",","")) if item["price"] != "NULL" else 'NULL'
        discount = int(item["discount"].split("%")[0]) if item["discount"] != "NULL" else 'NULL'
        rating = float(item["rating"]) if item["rating"] != "NULL" else 'NULL'
        

        self.corr.execute('''INSERT INTO 
        PRODUCTDESC(pnum,price,discount,rating,n_ratings,n_reviews)
              VALUES (?,?,?,?,?,?)''',(item["pnum"],price,discount,rating,item['n_ratings'],item['n_reviews']))
        
        self.conn.commit()
        
        brand = item["brand"].split(" ")[0] if item["brand"] != 'NULL' else 'NULL'

        ssd = item['SSD_Capacity'].split(" ") if item.get('SSD_Capacity',0) != 0 else 0

        if ssd !=0 and ssd[1] =='GB':
            SSD_Capacity_GB = int(ssd[0])
        elif ssd !=0 and ssd[1] =='TB': 
            SSD_Capacity_GB = int(ssd[0])*1000  
        else:
            SSD_Capacity_GB = 0

        hdd = item['HDD_Capacity'].split(" ") if item.get('HDD_Capacity',0) != 0 else 0

        if hdd !=0 and hdd[1] =='GB':
            HDD_Capacity_GB = int(hdd[0])
        elif hdd !=0 and hdd[1] =='TB': 
            HDD_Capacity_GB = int(hdd[0])*1000  
        else:
            HDD_Capacity_GB = 0
      
        RAM_GB = int(item['RAM'].split(" ")[0]) if item.get('RAM','NULL') != "NULL" else "NULL"
        ss = item['Screen_Size'].split(" ") if item.get('Screen_Size','NULL') != "NULL" else "NULL"
        if ss !='NULL' and ss[1] =='cm':
            Screen_Size_cm = float(ss[0])
        elif ss !='NULL' and ss[1] =='inch': 
            Screen_Size_cm = float(ss[0])*2.54   
        else:
            Screen_Size_cm = 'NULL'   

        self.corr.execute('''INSERT INTO 
        PRODUCTSPECS(pnum,brand,Model_Number,Type,Suitable_For,Processor_Brand,Processor_Name,SSD_Capacity_GB,
        HDD_Capacity_GB,RAM_GB,Graphic_Processor,Operating_System,Screen_Size_cm,Screen_Resolution)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (item["pnum"],brand,item.get('Model_Number','NULL'),item.get('Type','NULL'),item.get('Suitable_For','NULL'),item.get('Processor_Brand','NULL'),
        item.get('Processor_Name','NULL'),SSD_Capacity_GB,HDD_Capacity_GB,RAM_GB,item.get('Graphic_Processor','NULL'),item.get('Operating_System','NULL'),
        Screen_Size_cm,item.get('Screen_Resolution','NULL'))) 

        self.conn.commit()

class ProductReviewScraperPipeline:

    def __init__(self) :
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("product.db")
        self.corr = self.conn.cursor()

    def create_table(self):
        
        self.corr.execute('''DROP TABLE IF EXISTS PRODUCTREVIEWS''')
        self.corr.execute('''
                          create table ProductReviews (  
                                        rid integer primary key,   
                                        pnum integer not null,  
                                        review_rating integer,
                                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP not null, 
                                        review_date text,
                                        location text,
                                        review_title text,
                                        review text,
                                        foreign key (pnum) references productlink (pnum)
                                        ); 
                          ''')


    def process_item(self, item, spider):
        self.store_item(item)
        return item
    
    def store_item(self,item):
        
        if item["location"][:2] == ", ":
            item["location"] = item["location"][2:]



        self.corr.execute('''INSERT INTO PRODUCTREVIEWS(pnum,review_rating,review_date,location,review_title,review)
             VALUES (?,?,?,?,?,?)''',(item["pnum"],item["review_rating"],item["review_date"],item["location"],item["review_title"],item["review"]))
        self.conn.commit()


