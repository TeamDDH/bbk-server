

class Database:
    def __init__(self):
            self.conn= MySQLdb.connect(
            host='',
            port = 3306,
            user='root',
            passwd='',
            db ='bbk',
            charset='utf8',)
         self.user_list = []

    def get_mysql_user(self,begin,end):

        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM bbk WHERE ID >= "+str(begin) +" AND ID <= "+str(end) )
            rows = cur.fetchall()
            dict_uid = dict()
            # print rows
            for row in rows:
                # print "%s %s" % (row["user_id"], row["user_name"])
                # print "%s" % (row["user_id"])
                self.user_list.append(row["user_id"])
            # print user_list
            # dict_uid[row["user_id"]]=row["user_name"]
            return self.user_list