import requests

def get_vendor(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response)
        return "Unknown"
    vendor_info = response.text
    return vendor_info
