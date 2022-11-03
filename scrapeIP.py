import requests
import sys
import re

# TODO
# data visualiseren met hoeveel procent van welke landen etc.
# % of revisions annonymous
# Only include revisions made by IPs in API query
# >249 calls b2b error/ crash afhandelen
# parse monthly wikipedia datadumps
# IPINFO database
# EDIT database
# TAGSPEREDIT database
# Snellere versie in C#, C++ OID schrijven
# databse op rasppi hosten en daarnaar uploaden
# Andere talen ondersteunend

IPV4REGEX = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
IPV6REGEX = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
URL = "https://en.wikipedia.org/w/api.php"


class PageRevs:
    def __init__(self):
        self.anon_revs = []
        self.total_revs = 0
        self.ses = requests.Session()
        self.title = "TMP"  # TODO title fix
        self.page_id = self.get_page_id()
        self.params = {
            "action": "query",
            "prop": "revisions",
            "titles": "2020 Nagorno-Karabakh war",
            "rvlimit": 500,
            "rvprop": "ids|flags|timestamp|user|userid|size|comment|tags",
            "format": "json"
        }

    # Gets all revisions made by
    def get_revs(self, rvcont:str=""):
        # Adds continue value to params if needed.
        if rvcont != "":
            new_params = self.params.copy()
            new_params["rvcontinue"] = rvcont
        else:
            new_params = self.params.copy()

        # Gets json encoded content of response of the get request.
        data = self.ses.get(url=URL, params=new_params).json()

        # gets all revisions made by an annonymous user.
        revisions = data["query"]["pages"][self.page_id]["revisions"]
        for rev in revisions:
            self.total_revs += 1
            matchipv4 = re.search(IPV4REGEX, rev["user"])
            matchipv6 = re.search(IPV6REGEX, rev["user"])
            if matchipv4 or matchipv6:
                if rev not in self.anon_revs:
                    self.anon_revs.append(rev)

        # Gets continue value and calls function again if not all data is read.
        # Maximum API calls is 249.
        rvcontnew = data["continue"]["rvcontinue"]
        if rvcontnew != "":
            try:
                self.get_revs(rvcont=rvcontnew)
            except Exception:
                return

        return

    def get_page_id(self):
        id_params = {
            "action": "query",
            "prop": "info",
            "titles": "2020 Nagorno-Karabakh war",  # TODO title fix
            "format": "json"
        }
        data = self.ses.get(url=URL, params=id_params).json()
        id = list(data["query"]["pages"].keys())[0]

        return id


def main():
    p = PageRevs()
    p.get_revs()

    # print(p.total_revs)
    # print(len(p.anon_revs))
    print(p.anon_revs[0])
    print(p.anon_revs[1])
    print(p.anon_revs[2])
    print(p.anon_revs[3])
    print(p.anon_revs[4])
    print(p.anon_revs[5])


if __name__ == "__main__":
    main()
    # if len(sys.argv) == 2:
    #     url = sys.argv[1]
    #     main(url)
    # else:
    #     print("Please pass a Wikipedia url as an argument.")
