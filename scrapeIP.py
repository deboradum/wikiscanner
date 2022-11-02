import requests
import sys
import re

# TODO
# data visualiseren met hoeveel procent van welke landen etc.
# % of revisions annonymous
# Only include revisions made by IPs in API query

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
TOTAL = 0

# Gets all revisions made by
def get_revs(revs:list, rvcont:str=""):
    ses = requests.Session()
    if rvcont != "":
        new_params = PARAMS.copy()
        new_params["rvcontinue"] = rvcont
    else:
        new_params = PARAMS.copy()

    # Gets json encoded content of response of the get request.
    data = ses.get(url=URL, params=new_params).json()

    # Gets page ID
    page_id = list(data["query"]["pages"].keys())[0]

    # gets all revisions made by an annonymous user.
    revisions = data["query"]["pages"][page_id]["revisions"]
    for rev in revisions:
        matchipv4 = re.search(IPV4REGEX, rev["user"])
        matchipv6 = re.search(IPV6REGEX, rev["user"])
        if matchipv4 or matchipv6:
            if rev not in revs:
                revs.append(rev)

     # Gets continue value
    rvcontnew = data["continue"]["rvcontinue"]
    if rvcontnew != "":
        try:
            get_revs(revs, rvcont=rvcontnew)
        except Exception:
            pass


def main():
    revs = []

    get_revs(revs)


if __name__ == "__main__":
    main()
    # if len(sys.argv) == 2:
    #     url = sys.argv[1]
    #     main(url)
    # else:
    #     print("Please pass a Wikipedia url as an argument.")
