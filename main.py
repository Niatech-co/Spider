# main.py
import os
import logging
from scrapy.crawler import CrawlerProcess
from petroleum_spider import PetroleumCompanySpider
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def start_crawl(keyword, location):
    logger.info(f"Starting crawl with keyword: {keyword} and location: {location}")
    
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        logger.error("SERPAPI_KEY not found in environment variables.")
        return

    # Translate keyword
    try:
        translated_keyword = GoogleTranslator(source="auto", target=location).translate(keyword)
        logger.info(f"Translated keyword: {translated_keyword}")
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return

    # Setup Scrapy crawler process
    process = CrawlerProcess(settings={
        'FEEDS': {
            "output.json": {"format": "json"},
        },
        'DEPTH_LIMIT': 2,
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'DOWNLOAD_DELAY': 0.25,
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 86400,
        'HTTPCACHE_DIR': 'httpcache',
        'CLOSESPIDER_PAGECOUNT': 1000,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })

    # Run the crawler
    logger.info("Starting the Scrapy crawler process...")
    process.crawl(PetroleumCompanySpider, keyword=translated_keyword, location=location, api_key=api_key)
    process.start()
    logger.info("Crawler process finished.")
    return True  # Return True if crawl was successful


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="Keyword for the crawler")
    parser.add_argument("--location", help="Location for the crawler")
    args = parser.parse_args()

    if args.keyword and args.location:
        success = start_crawl(args.keyword, args.location)
        if success:
            logger.info("Crawl completed successfully.")
        else:
            logger.error("Crawl failed.")
