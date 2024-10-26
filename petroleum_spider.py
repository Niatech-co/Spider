import scrapy
from scrapy.http import Request

class PetroleumCompanySpider(scrapy.Spider):
    name = "petroleum_spider"
    allowed_domains = ["serpapi.com"]
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "ROBOTSTXT_OBEY": False,
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,  # Retry on failure
    }

    def __init__(self, keyword, location, api_key, *args, **kwargs):
        super(PetroleumCompanySpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.location = location
        self.api_key = api_key
        self.start_urls = [
            f"https://serpapi.com/search?q={keyword}+companies+in+{location}&api_key={api_key}&num=100"
        ]

    def parse(self, response):
        # Check response status before processing
        if response.status == 403:
            self.logger.error(f"Access forbidden: {response.url}")
            return
        elif response.status != 200:
            self.logger.error(f"Non-200 status: {response.status}")
            return

        # Parse JSON response for data
        json_data = response.json()
        if "organic_results" in json_data:
            for result in json_data["organic_results"]:
                title = result.get("title", "")
                link = result.get("link", "")
                snippet = result.get("snippet", "")

                # Yield each extracted item as a dictionary
                yield {
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                }

        else:
            self.logger.warning("No 'organic_results' found in JSON response")
