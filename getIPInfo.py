import requests
import time

# Returns a dictionary containg information about the IP address.
def get_ips_info(ips):
    s = requests.Session()
    ips_info = []

    for ip in ips:
        time.sleep(0.24)
        data = s.get(url=f"https://ipapi.co/{ip}/json/").json()
        if data.get("reason") != 'RateLimited':
            ips_info.append(data)
        else:
            print(f"Rate limited by ipapi. IP {ip} not added.")

    return ips_info
