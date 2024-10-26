# pipelines.py

import os
from scrapy.exceptions import DropItem  # Import DropItem here

class DuplicatesPipeline:
    def __init__(self):
        self.seen_urls = set()
        self.file_path = "scraped_urls.txt"
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.seen_urls = set(line.strip() for line in f)

    def process_item(self, item, spider):
        if item['link'] in self.seen_urls:
            raise DropItem(f"Duplicate item found: {item['link']}")
        else:
            self.seen_urls.add(item['link'])
            with open(self.file_path, 'a') as f:
                f.write(item['link'] + "\n")
            return item
