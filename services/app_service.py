import requests

def fetch_api_data(api_url):
    """
    Fetch data from the API and return the JSON response.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return {}