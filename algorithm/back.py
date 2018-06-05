import requests,sys,os,time,json
from wb_db import Mysql

file_path =os.path.join(sys.path[0],"test.txt")

file=open(file_path,'r',enco ding='utf-8')
for line in file.readlines():
    uid="null"
    screen_name="null"
    description="null"
    article = "null"
    comment = "null"

    if line:
        list=[]
        list=line.encode('utf-8').decode('utf-8-sig').strip('\n').split("________")
        uid = list[0] if len(list[0])>0 else "null"
        screen_name = list[1] if len(list[1])>0 else "null"
        description = list[4] if len(list[4])>0 else "null"
        article = list[4] if len(list[4]) > 0 else "null"
        comment = list[4] if len(list[4]) > 0 else "null"
        sql = ""
            insert into bbk (uid,screen_name,description,article,comment) VALUES ('%s','%s','%s','%s','%s')""

        try:
            mysql = Mysql()
            mysql.execute_no_query(sql % (uid,screen_name,description,article,comment))
        except Exception as e:
            print(e)
        finally:
            mysql.db_close()
    else:
        break