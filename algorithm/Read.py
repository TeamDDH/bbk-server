import pandas as pd

conn = mysql.connect(
    host="localhost",
    database="bbk",
    user="root",
    password="",
    port=3306,
    charset='utf8'
)

sqlcmd = "select col_name,col_type,col_desc from itf_datadic_dtl_d limit 10"

a = pd.read_sql(sqlcmd, dbconn)

b = a.head()
print(b)


# pd.read_csv()

# pd.read_excel()

# pd.read_table()