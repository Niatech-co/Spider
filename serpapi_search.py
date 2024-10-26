# petroleum_spider.py

import scrapy
from scrapy.exceptions import DropItem

class PetroleumCompanySpider(scrapy.Spider):
    name = "petroleum_company"
    seen_urls = set()  # Set to store seen URLs
    
    def __init__(self, keyword, location, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.location = location
        self.api_key = api_key

    def parse(self, response):
        # Assuming each result has a URL
        for result in response.json()['organic_results']:
            url = result.get('link')
            if url in self.seen_urls:
                self.logger.debug(f"Duplicate found, skipping: {url}")
                continue
            self.seen_urls.add(url)
            yield {
                'title': result.get('title'),
                'link': url,
                'snippet': result.get('snippet')
            }
