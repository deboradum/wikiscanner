Wikiscanner is a program that scans Wikipedia pages for annonymous revisions. Annonymous revisions are revisions that were made without an account.
When an annonymous revision is made, the IP address of the device that made the revision is shown.
This program collects these IP addresses and analyzes them to retrieve information about the location and organization that made the edit.

The goal of this project is to improve transparency in Wikipedia pages by collecting information about who made the edits.

The revision data is collected using the MediaWiki API (https://www.mediawiki.org/wiki/API:Main_page).
Keep in mind that there is a maximum of 249 requests at a time for the API. Pages with more than 12,450 edits will thus not collect all the edits.

The information about IPs is collected using ipapi (https://ipapi.co/). This API has a maximum of 1,000 requests per day, and 30,000 per month per IP.

The IP shown at a revision gives information about what network the edit came from. An edit that came from a specific organization does not automatically mean that the organization made the edit. It merely means that the revision came from a device connected to the organization's network.

This project was inspired by Virgil Griffith's WikiScanner (https://en.wikipedia.org/wiki/WikiScanner).
