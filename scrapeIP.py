import requests
import sys
import re


# TODO
# Make checking work for all Wikipedia languages
# data visualiseren met hoeveel procent van welke landen etc.
# IPv4 en IPv6 regex

IPV4REGEX = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
IPV6REGEX = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {
        "action": "query",
        "prop": "revisions",
        "titles": "2020 Nagorno-Karabakh war",
        "rvlimit": 500,
        "format": "json"
    }

def main():
    ses = requests.Session()
    revs = []

    # Gets json encoded content of response of the get request.
    data = ses.get(url=URL, params=PARAMS).json()

    # NOG IETS ANDERS OP VINDEN OM PAGE ID TE KRIJGEN
    x = data["query"]["pages"]
    for y in x:
        page_id = y
        break

    revisions = data["query"]["pages"][page_id]["revisions"]
    # gets all revisions made by an annonymous user.
    for rev in revisions:
        matchipv4 = re.search(IPV4REGEX, rev["user"])
        matchipv6 = re.search(IPV6REGEX, rev["user"])
        if matchipv4 or matchipv6:
            revs.append(rev)
    print(revs)


if __name__ == "__main__":
    main()
    # if len(sys.argv) == 2:
    #     url = sys.argv[1]
    #     main(url)
    # else:
    #     print("Please pass a Wikipedia url as an argument.")
