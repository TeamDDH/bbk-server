# bbk-server

> Server of bbk. bbk is a Topic Detection and Tracking (TDT) system.

This system is devided into three parts:

1.  A web server.
2.  An algorithm core.
3.  Some spiders.

and celery as their glue!

We also have a simple client for this. [Check it out](https://github.com/TeamDDH/bbk-rn).

## Build Process

1.  Set up a virtual env (optional).
2.  `pip install -r config/requirements.txt` to install all dependencies.
3.  Install MySQL and create two databases: `bbk`, `bbkserver`, and make sure the database uri in file `.config` is correct. (`bbkserver` is for the web server. `bbk` is for the algorithm module and spiders)
4.  Install Redis.
5.  `python manage.py db init` `python manage.py db migrate` `python manage.py db upgrade`

Then:

1.  `python manage.py server` to start server.
2.  `scrapy crawl XXX` to start a spider.

I will provide a `fabfile` later to make this easier.

---

TeamDDH, 2018.
