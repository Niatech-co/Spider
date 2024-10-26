# settings.py
ITEM_PIPELINES = {
    'yourproject.pipelines.DuplicatesPipeline': 100,
}

# Set a user agent to avoid being blocked
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

# Avoid using outdated REQUEST_FINGERPRINTER_IMPLEMENTATION
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

# Add download delay to avoid overloading servers
DOWNLOAD_DELAY = 2  # Adjust as needed

# Retry settings in case of failure
RETRY_ENABLED = True
RETRY_TIMES = 3  # Number of retries for failed requests

# Optional: Log level for debugging
LOG_LEVEL = 'DEBUG'
