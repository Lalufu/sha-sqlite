#!/usr/bin/env python3
"""
Insert COUNT sha1 hashes into the sha tabke of the sha.sqlite database in the
current directory.

The table must exist (use "mysql lalufu < sha.sql" to create
it.

=====

Test Run: Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz (8 Threads), 
          32GB RAM, 
          Crucial M4-CT512M4SSD2

Sample run with
mysql> SET GLOBAL key_buffer_size = 16*1024*1024*1024;

$ ./sha-create.py
0...100000 [...]35900000...
2273.43 seconds, 15835.10 inserts/s
Created index in 131.92 seconds

mysql> select table_name
            , engine
            , row_format
            , table_rows
            , data_length/1024/1024 as data_mb
            , index_length/1024/1024 as index_mb
         from information_schema.tables
where table_name ='sha';
+------------+--------+------------+------------+---------------+---------------+
| table_name | engine | row_format | table_rows | data_mb       | index_mb      |
+------------+--------+------------+------------+---------------+---------------+
| sha        | MyISAM | Dynamic    |   36000000 | 1785.27832031 | 1894.82910156 |
+------------+--------+------------+------------+---------------+---------------+
1 row in set (0.00 sec)


"""

import hashlib
import MySQLdb
import time

HOST   = "localhost"
USER   = "lalufu"
PASSWD = "keks"
DB     = "lalufu"

COUNT = 36000000

def main():
    conn = MySQLdb.connect(user=USER, passwd=PASSWD, db=DB, host=HOST)

    c = conn.cursor()

    start = time.time()

    for i in range(0, COUNT):
        c.execute("""
          INSERT INTO `sha` (`sha`) VALUES (%s)
        """, (hashlib.sha1(b'%d' % (i,)).hexdigest(),))

        if i % 100000 == 0:
            print('%d...' % (i,), end='', flush=True)
            conn.commit()

    conn.commit()
    end = time.time()

    print()
    print('%.2f seconds, %.2f inserts/s' % (end-start, COUNT / (end-start)))

    start = time.time()
    c.execute("""
        ALTER TABLE `sha` ADD INDEX `sha` ( `sha` )
        """)
    end = time.time()
    print('Created index in %.2f seconds' % (end-start,))

    conn.close()

if __name__ == "__main__":
    main()
