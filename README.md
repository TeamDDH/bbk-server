# bbk-server

> Server of bbk.

## Build Process

1.  Set up a virtual env (optional).
2.  `pip install -r config/requirements.txt`
3.  Install MySQL and create two databases: `bbk`, `bbkserver`, and make sure the database uri in file `.config` is correct.
4.  Install Redis.
5.  `python manage.py db init`

Then:

1.  `python manage.py server` to start server.
2.  `scrapy crawl XXX` to start a spider.

---

TeamDDH, 2018
