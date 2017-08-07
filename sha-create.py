#!/usr/bin/python3
"""
Insert COUNT sha1 hashes into the sha tabke of the sha.sqlite database in the
current directory.

The table must exist (use "sqlite3 sha.sqlite < sha.sql" to create
it.
"""

import hashlib
import sqlite3
import time

COUNT = 36000000

def main():
    conn = sqlite3.connect('sha.sqlite')

    c = conn.cursor()
    c.execute('PRAGMA synchronous=off')
    c.execute('PRAGMA count_changes=OFF')

    start = time.time()

    for i in range(0, COUNT):
        c.execute("""
            INSERT INTO `sha`
                        ('sha')
                 VALUES (?)
                 """, (hashlib.sha1(b'%d' % (i,)).hexdigest(),))

        if i % 100000 == 0:
            now = time.time()
            print('%d rows, %.2f seconds, %.2f inserts/s' % (i, now-start, COUNT / (now-start)), flush=True)
            # conn.commit()

    conn.commit()
    end = time.time()

    print()
    print('%.2f seconds, %.2f inserts/s' % (end-start, COUNT / (end-start)))

    start = time.time()
    c.execute("""
        CREATE INDEX "sha_index"
                  ON "sha" ("sha")
        """)
    end = time.time()
    print('Created index in %.2f seconds' % (end-start,))

    conn.close()

if __name__ == "__main__":
    main()
