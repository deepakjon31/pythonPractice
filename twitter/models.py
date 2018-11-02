import sqlite3
import pickle


con = sqlite3.connect('tweets.db')
cur = con.cursor()
# cur.execute('drop table pickled')
# cur.execute("create table pickled(id integer primary key, data blob)")
# cur.execute("insert into pickled(data) values (?)", (sqlite3.Binary(pickle.dumps(item, protocol=2)),))


cur.execute('select data from pickled')
print(cur.fetchall())
for row in cur:
    serialized = row[0]
    point = pickle.loads(serialized)
    print(type(point), point)


con.close()