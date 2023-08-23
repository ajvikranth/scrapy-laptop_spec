# scrapy-laptop_specs_and_reviews

This repository contains a Scrapy project for scraping laptop links, specifications, and reviews from the Flipkart ecommerce website. The scraped data is then stored in a SQLite database. This project runs in Conda environment.

## Project Structure

The project structure is organized as follows:

- spiders/
  - product_desc_spider.py
  - product_link_spider.py
  - product_review_spider.py
- __pycache__/
- items.py
- middlewares.py
- pipelines.py
- settings.py
- __init__.py
- requirements.txt


Scrapy Flipkart Laptop Scraper
This repository contains a Scrapy project for scraping laptop links, specifications, and reviews from the Flipkart ecommerce website. The scraped data is then stored in a SQLite database. This project is designed to run within a Conda environment.

Project Structure
The project structure is organized as follows:

- spiders/
  - product_desc_spider.py
  - product_link_spider.py
  - product_review_spider.py
- __pycache__/
- db.py
- items.py
- middlewares.py
- pipelines.py
- settings.py
- __init__.py
- spec-file.txt
  
spiders/: This directory contains the Scrapy spiders responsible for different stages of scraping:

product_desc_spider.py: Scrapes laptop specifications.
product_link_spider.py: Extracts laptop product links.
product_review_spider.py: Collects laptop reviews.
pycache/: A directory for Python bytecode files.

items.py: Defines the data structure (items) for scraped information.

middlewares.py: Middleware configuration for Scrapy.

pipelines.py: Custom pipelines to process and store scraped data.

settings.py: Scrapy project settings.

init.py: Empty initialization file for the package.

spec-file.txt: File listing all the required dependencies to set up the Conda environment.

## Usage
- Clone the repository:
   ```bash
   git clone https://github.com/ajvikranth/scrapy-laptop_specs_and_reviews.git
   ```

- Create and activate a Conda environment (assuming you have Conda installed):
   ```bash
   conda create --name myenv --file spec-file.txt
   conda activate myenv
   ```
- Adjust the spider configurations and settings in the respective spider files if needed.
- Run the spiders using the following commands:
   ```bash
   scrapy crawl ProductLinks
   scrapy crawl ProductDesc
   scrapy crawl ProductReview

   ```
   note: use the spiders in this order as ProductDesc and ProductReview get the links to crawl from a table created by ProductLinks spider.
The scraped data will be stored in the SQLite database as defined in scrapy pipeline.py file.

## Note:
This project is intended for study purposes only. Please respect the terms of use of the targeted website.
  
