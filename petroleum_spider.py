import json
import scrapy

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
        self.results = []  # Initialize a list to hold results

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"Request failed with status: {response.status}")
            return

        # Parse JSON response
        json_data = response.json()
        if "organic_results" in json_data:
            for result in json_data["organic_results"]:
                self.results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                })

            # Save results after parsing is complete
            if self.results:
                save_results(self.results)
        else:
            self.logger.warning("No 'organic_results' found in JSON response")

# Define the save_results function outside of the class
def save_results(data):
    # Write only when there's data, avoiding overwriting with empty lists
    if data:
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
