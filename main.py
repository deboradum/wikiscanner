import databaseHandler
import scrapeIP
import getIPInfo

# TODO
# data visualiseren met hoeveel procent van welke landen etc.
# % of revisions annonymous
# Only include revisions made by IPs in API query
# >249 calls b2b error/ crash afhandelen
# parse monthly wikipedia datadumps
# Snellere versie in C#, C++ OID schrijven
# Andere talen ondersteunend
# IPAPI error handling
# custom title fixen!

def main():
    wiki_handler = scrapeIP.WikiAPIHandler()
    wiki_handler.get_revs()

    db = databaseHandler.Database()
    # Inserts ip infos to database.
    ips_info = getIPInfo.get_ips_info(wiki_handler.get_ips())
    db.insert_ip(ips_info)
    # Inserts revisions to database.
    db.insert_revision(wiki_handler.anon_revs)
    # Closes connection to database.
    db.destroy()


if __name__ == "__main__":
    main()
    # if len(sys.argv) == 2:
    #     url = sys.argv[1]
    #     main(url)
    # else:
    #     print("Please pass a Wikipedia url as an argument.")
