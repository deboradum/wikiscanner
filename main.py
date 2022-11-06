import databaseHandler
import scrapeIP

def main():


    db = databaseHandler.Database()
    print(db)
    db.get_version()


    # p = scrapeIP.PageRevs()

    # p.get_revs()
    # print(p.anon_revs[0])
    # print("")
    # ips_info = getIPInfo.get_ip_info(p.get_ips())
    # print(ips_info[0])


if __name__ == "__main__":
    main()
    # if len(sys.argv) == 2:
    #     url = sys.argv[1]
    #     main(url)
    # else:
    #     print("Please pass a Wikipedia url as an argument.")
