import sqlite3

conn = sqlite3.connect("product.db")
cur = conn.cursor()
# cur.execute('''
# create table ProductReviews (  
#             rid integer primary key,   
#             pnum integer not null,  
#             review_rating integer,
#             Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP not null, 
#             review_date text,
#             location text,
#             review_title text,
#             review text,
#             foreign key (pnum) references productlink (pnum)
#             );
# ''')

# cur.execute('''INSERT INTO PRODUCTREVIEWS(pnum,review_rating,review_date,location,review_title,review)
#              VALUES (?,?,?,?,?,?)''',(1,1,'3 months ago',"Pune","Very poor","Worst"))


cur.execute("select * from PRODUCTREVIEWS; ")
rows = cur.fetchall()
print(rows[962][0])