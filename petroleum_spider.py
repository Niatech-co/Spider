# petroleum_spider.py
import scrapy
from serpapi_search import get_search_results

class PetroleumCompanySpider(scrapy.Spider):
    name = "petroleum_spider"

    def __init__(self, keywordOne, keywordTwo,location, api_key, *args, **kwargs):
        super(PetroleumCompanySpider, self).__init__(*args, **kwargs)
        # Fetch URLs using SerpAPI with the given keyword and location
        self.start_urls = get_search_results(keywordOne, keywordTwo, location, api_key)

    def parse(self, response):
        # Example parsing logic to extract company details
        company_name = response.xpath('//h1/text()').get() or response.xpath('//title/text()').get()
        description = response.xpath('//meta[@name="description"]/@content').get()
        address = response.xpath('//address//text()').get()

        if company_name and "Vietnam" in response.text:
            yield {
                'company_name': company_name.strip(),
                'description': description.strip() if description else 'N/A',
                'address': address.strip() if address else 'N/A',
                'url': response.url,
            }

        # Optionally, follow links to other pages to find more companies
        for href in response.xpath('//a/@href').getall():
            yield response.follow(href, self.parse)
