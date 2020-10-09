import sqlite3 as sql
import random
from pprint import pprint


def conct(db_file:str ='db_file.sqlite3'):
    """Connect to a sqlite database file."""
    return sql.connect(db_file)


def table_exists(cursor, table_name='test_table'):
    # check if table exists
    # check_query = """SELECT * FROM sqlite_master WHERE  type='table' AND name={tbl};""".format(tbl=table_name)
    check_query = """SELECT * FROM sqlite_master"""  # WHERE  type='table' AND name={tbl};""".format(tbl=table_name)


    # TODO: trying to get the headers, it looks like they're in the tuple in the cursor?
    result = cursor.execute(check_query)
    print(cursor)
    for row in result.fetchall():
        print(row)


# connect to the db
con = conct()

# instantiate a cursor
cur = con.cursor()

# mk_tbl = """
#     CREATE TABLE test_table (
#         id integer PRIMARY KEY,
#         text_col TEXT NOT NULL,
#         num_col integer NOT NULL)
#         """
#
# rnd_lists = [str(num) for num in (random.randint(0, 200), random.randint(0, 200))]
# # print(rnd_lists)
#
#
# in_tbl = """
#     INSERT INTO test_table(num_col, text_col) VALUES({rnd}, '{word}');
# """.format(rnd=random.randint(0, 1000), word=''.join(rnd_lists))
#
# # print('insert text', in_tbl)
#
# # insert
# res = cur.execute(in_tbl)
# # print(res.fetchall())
# # print(cur.rowcount)
#
# # select
# sl_tbl = """
# SELECT * FROM test_table"""
# res = cur.execute(sl_tbl)
# # print('after', res.fetchall())
# # print(cur.description)

_ = table_exists(cur)
