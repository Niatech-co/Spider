# main.py
from scrapy.crawler import CrawlerProcess
from petroleum_spider import PetroleumCompanySpider

# Replace with actual values
keywordOne = "lubricant"
keywordTwo = "companies"
location = "Vietnam"
api_key = "d8eed6fbde7098cd8ad630ba875841248c1fb71ed24c6e6db0e15ddbb487098d"  # Your SerpAPI key

# Set up the Scrapy crawler process
process = CrawlerProcess(settings={
    "FEEDS": {
        "output.json": {"format": "json"},
    },
})

# Run the spider, passing the required arguments (keyword, location, and api_key)
process.crawl(PetroleumCompanySpider, keywordOne=keywordOne, keywordTwo = keywordTwo, location=location, api_key=api_key)
process.start()
