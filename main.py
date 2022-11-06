import databaseHandler
import scrapeIP
import getIPInfo
import argparse

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
