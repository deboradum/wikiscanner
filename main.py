import databaseHandler
import scrapeIP
import getIPInfo
import argparse

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

def main(title=None, id=None):
    wiki_handler = scrapeIP.WikiAPIHandler(title=title, id=id)
    wiki_handler.get_revs()

    db = databaseHandler.Database()
    # Inserts ip infos to database.
    ips_info = getIPInfo.get_ips_info(wiki_handler.get_ips())
    db.insert_ip(ips_info)
    # Inserts revisions to database.
    db.insert_revision(wiki_handler.anon_revs)
    # Closes connection to database.
    db.destroy()

    print("Added data to database.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', "--title", help="Title of the page.")
    group.add_argument("-id", help="Page id of the page.")

    args = parser.parse_args()

    main(title=args.title, id=args.id)
