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

    p = scrapeIP.PageRevs()
    p.get_revs()

    db = databaseHandler.Database()
    ips_info = getIPInfo.get_ips_info(p.get_ips())
    # db.insert_ip(ips_info)

    db.insert_revision(p.anon_revs)

    db.destroy()



if __name__ == "__main__":
    main()
    # if len(sys.argv) == 2:
    #     url = sys.argv[1]
    #     main(url)
    # else:
    #     print("Please pass a Wikipedia url as an argument.")
