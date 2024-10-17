import requests, os


API_KEY = os.getenv("IPFIND_API_KEY")

def get_location_from_ip(ip_address):
    """Fetch location data from an IP address."""
    try:
        response = requests.get(f"https://api.ipfind.com?ip={ip_address}&auth={API_KEY}")

        if response.status_code == 200:
            data = response.json()
            # Extract the desired fields
            return {
                "city": data.get("city", "Unknown"),
                "country": data.get("country", "Unknown"),
                "latitude": data.get("latitude", None),
                "longitude": data.get("longitude", None),
            }
    except Exception as e:
        print(f"Failed to get location: {e}")
    return {
        "city": "Unknown",
        "country": "Unknown",
        "latitude": None,
        "longitude": None,
    }
