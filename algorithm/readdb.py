import MySQLdb
import sys
import os
from lxml import etree

IP=sys.argv[1]
#IP="10.0.20.252"
DIR="ScriptsDir"
try:
    print "connnect to database...."
    db=MySQLdb.connect(IP,"root"," ","bbk")
except Exception as e:
    print e.message
    print "Can't connect to " + IP
    exit(1)

print "Done...."
print "Ready to read data from DataBase......"
db_cursor=db.cursor()

sql="select Description,TestScript from Script where Class='System'"
db_cursor.execute(sql)
content=db_cursor.fetchall()
if os.path.exists(DIR):
   os.system("RD /S /Q " + DIR)
os.system("mkdir " + DIR)
for item in content:
    file_name=item[0]
    if len(file_name)==0:
        print item
        continue

    directory=item[0].split(".")[0]
    if len(directory)==0:
        print item
        continue
    if not os.path.exists(DIR+"\\"+directory):
        os.system("mkdir " + DIR + "\\"+directory)
    try:
        f=open(DIR+"\\"+directory+"\\"+file_name+".xml","w")
        root=etree.fromstring(item[1])
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write(etree.tostring(root))
        f.close()
    except Exception as e:
        print e.message
        print "Failed,please retry...."
        break;
print "See Scripts data file in '" + DIR + "'"
print "Done"