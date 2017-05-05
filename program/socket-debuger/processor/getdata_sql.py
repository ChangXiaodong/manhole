import MySQLdb

conn = MySQLdb.connect(
    host='121.42.213.241',
    port=3306,
    user='root',
    passwd='cxd',
    db='parkinfo',
)
cur = conn.cursor()
aa = cur.execute("select * from manhole_database_sensor")
info = cur.fetchmany(aa)
for ii in info:
    print(ii)
cur.close()
conn.commit()
conn.close()
