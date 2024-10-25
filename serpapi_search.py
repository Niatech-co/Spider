# serpapi_search.py
import requests

def get_search_results(keywordOne,keywordTwo, location, api_key):
    """
    Fetch search engine results for a given keyword and location using SerpAPI.
    """
    params = {
        "q": f"{keywordOne,keywordTwo} companies in {location}",
        "api_key": api_key,
        "num": 10
    }
    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json().get('organic_results', [])
    return [result['link'] for result in results if 'link' in result]

if __name__ == "__main__":
    # Example usage
    keywordOne = "lubricant"
    keywordTwo = "companies"
    location = "Vietnam"
    api_key = "d8eed6fbde7098cd8ad630ba875841248c1fb71ed24c6e6db0e15ddbb487098d"  # Replace with your actual SerpAPI key
    urls = get_search_results(keywordOne,keywordTwo, location, api_key)
    print("Matching URLs:", urls)
