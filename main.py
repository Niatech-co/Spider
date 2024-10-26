import os
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from petroleum_spider import PetroleumCompanySpider
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Dictionary of supported languages for selection
languages = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 
    'vietnamese': 'vi', # Include the most relevant ones here...
    'english': 'en', 'french': 'fr', 'german': 'de', 'japanese': 'ja', 'korean': 'ko'
    # Add more if needed
}

# Prompt the user to enter the phrase and target location
phrase = input("Enter the phrase describing the target companies: ")
print("Available languages:", languages)
selected_language = input("Enter the language code for the target location (e.g., 'vi' for Vietnamese): ")

# Validate the selected language
if selected_language not in languages.values():
    print("Invalid language code. Please restart and select a supported code.")
    exit()

# Manual keyword optimization (splits the phrase into keywords)
def optimize_keywords_manually(phrase):
    return phrase.split()

optimized_keywords = optimize_keywords_manually(phrase)
print("Optimized Keywords:", optimized_keywords)

# Translate keywords to the selected language
translated_keywords = [GoogleTranslator(source="en", target=selected_language).translate(keyword) for keyword in optimized_keywords]
print("Translated Keywords:", translated_keywords)

# Check if keywords are available
if translated_keywords:
    api_key = os.getenv("SERPAPI_KEY")  # Add your SERPAPI_KEY to .env
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},
        },
        "RETRY_TIMES": 3,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })

    for keyword in translated_keywords:
        process.crawl(PetroleumCompanySpider, keyword=keyword, location=selected_language, api_key=api_key)
    process.start()
else:
    print("No keywords to process for the crawl.")
