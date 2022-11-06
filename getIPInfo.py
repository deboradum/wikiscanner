import requests

# Returns a dictionary containg information about the IP address.
def get_ips_info(ips):
    s = requests.Session()
    ips_info = []

    for ip in ips:
        data = s.get(url=f"https://ipapi.co/{ip}/json/").json()
        ips_info.append(data)

    return ips_info
