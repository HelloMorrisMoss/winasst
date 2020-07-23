import sqlite3 as sql
import random

def conct():
    return sql.connect('db_file.sqlite3')

con = conct()

cur = con.cursor()

chk_tbl = """SELECT name FROM sqlite_master WHERE  type='table' AND name='test_table';"""

mk_tbl = """
    CREATE TABLE test_table (
        id integer PRIMARY KEY,
        text_col TEXT NOT NULL,
        num_col integer NOT NULL)
        """

in_tbl = """
    INSERT INTO test_table(num_col, text_col) VALUES({rnd}, '{word}');
""".format(rnd=random.randint(0, 1000), word=''.join([chr(num).encode('ascii', 'ignore') for num in (random.randint(0, 200), random.randint(0, 200))]))

print('insert text', in_tbl)

sl_tbl = """
SELECT * FROM test_table"""

res = cur.execute(in_tbl)
print(res.fetchall())
print(cur.rowcount)
res = cur.execute(sl_tbl)
print('after', res.fetchall())
print(cur.description)