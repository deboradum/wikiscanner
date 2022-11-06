import requests
import re
from dotenv import load_dotenv
import getIPInfo
from databaseHandler import Database

IPV4REGEX = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
IPV6REGEX = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

class PageRevs:
    def __init__(self):
        self.anon_revs = []
        self.total_revs = 0
        self.ses = requests.Session()
        self.title = "2020 Nagorno-Karabakh war"  # TODO title fix
        self.params = {
            "action": "query",
            "prop": "revisions",
            "titles": self.title,
            "rvlimit": 500,
            "rvprop": "ids|flags|timestamp|user|userid|size|comment|tags",
            "format": "json"
        }
        self.page_id = self.get_page_id()

    # Gets all revisions made by annonymous users.
    def get_revs(self, rvcont:str=""):
        # Adds continue value to params if needed.
        if rvcont != "":
            new_params = self.params.copy()
            new_params["rvcontinue"] = rvcont
        else:
            new_params = self.params.copy()

        # Gets json encoded content of response of the get request.
        data = self.ses.get(url=WIKI_API_URL, params=new_params).json()

        # gets all revisions made by an annonymous user.
        revisions = data["query"]["pages"][self.page_id]["revisions"]
        for rev in revisions:
            self.total_revs += 1
            matchipv4 = re.search(IPV4REGEX, rev["user"])
            matchipv6 = re.search(IPV6REGEX, rev["user"])
            if matchipv4 or matchipv6:
                if rev not in self.anon_revs:
                    rev["page_id"] = self.page_id
                    rev["page_title"] = self.title
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

    # Gets page ID.
    def get_page_id(self):
        id_params = {
            "action": "query",
            "prop": "info",
            "titles": self.title,  # TODO title fix
            "format": "json"
        }
        data = self.ses.get(url=WIKI_API_URL, params=id_params).json()
        id = list(data["query"]["pages"].keys())[0]

        return id

    # Returns a list of the IP addresses that made revisions.
    def get_ips(self):
        ips = {dict["user"] for dict in self.anon_revs}

        return list(ips)

