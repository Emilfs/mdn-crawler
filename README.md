# mdn-crawler
mdn-crawler is a Crawler that is used for the migration of MDN Web Docs to Firefox Source Docs

```sh
$ cd crawler
$ pip install -r requirements.txt
```
To run the general crawler (still needs work)
```sh
$ scrapy crawl mdn
```
To run the csv crawler
```sh
$ scrapy crawl csv
```

### mdn

Given a starting url it will download the page that the url points to and convert the page to rst before saving it as an rst file. It will then crawl through every link on that page and do the same until there are no more links on the page or every link on the page has been accessed by the crawler before.

### csv
Given a CSV file containing url seperated by newline it will download the page that the url points to and convert the page to rst before saving it as an rst file. CSV files used are in topdir/crawler/crawler/csv/. migration_list.csv is gathered from [here][migration list]



mdn are not yet finished since the rules i defined for it are still a bit off. For now it's better to use the csv instead.

This is still a work in progress, any suggestions would be most welcome.
Contact me at chat.mozilla.org @emilfars

[migration list]: https://docs.google.com/spreadsheets/d/1q2ju9F-_PFRsPwwp3kKKaOebyQvbqwIGq-pRyMZdoPM/edit?usp=sharing