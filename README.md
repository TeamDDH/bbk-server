# bbk-server

该系统分为三个部分:

1. 一个 web 服务器
2. 算法核心
3. 爬虫

celery 用于计划任务和调度.

我们为这个系统建立了一个简单的[客户端](https://github.com/TeamDDH/bbk-rn).

## 构建过程

1. 可选, 创建一个虚拟环境.
2. `pip install -r config/requirements.txt` 来安装所有依赖.
3. 安装 MySQL 并创建两个数据库 `bbk-spider`, `bbk-server`, 确保 `.config` 文件中的数据库 uri 是正确的. 创建后配置正确的用户名和密码.
4. 安装 Redis.
5. `python manage.py db init` `python manage.py db migrate` `python manage.py db upgrade` 这些命令会初始化 `bbk-server`.

## 部署和工具

1. `python manage.py server` 来启动 web 服务器.
2. `scrapy crawl XXX` 来单独启动某个爬虫启动爬虫.
3. `python manage.py spider` 来启动所有的爬虫.

---

TeamDDH, 2018.
