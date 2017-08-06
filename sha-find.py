#!/usr/bin/python3
"""
Run COUNT queries for specific sha1 hashes against the sha.sqlite
database in the current directory.

Set RANGEMAX to the number of hashes that the database was filled with
using sha-create.py.

Queries will be made for random numbers between 0 and RANGEMAX*2,
the idea being that around half of the queries should result in hashes
that are not present, and half of them are.
"""

import hashlib
import sqlite3
import time
import random
import statistics

COUNT = 1000
RANGEMAX = 36000000

def main():
    conn = sqlite3.connect('sha.sqlite')

    c = conn.cursor()
    succtimes = []
    failtimes = []

    for i in range(0, COUNT):
        value = random.randint(0, (RANGEMAX*2)-1)

        start = time.time()
        c.execute("""
            SELECT 'id'
              FROM `sha`
             WHERE `sha` = ?
            """, (hashlib.sha1(b'%d' % (value,)).hexdigest(),))
        end = time.time()

        if c.fetchone() is None:
            # No entry found
            failtimes.append(end-start)
        else:
            succtimes.append(end-start)

        if i % 100 == 0:
            print('%d...' % (i,), end='', flush=True)

    print()
    conn.close()

    print('success: %d/%d' % (len(succtimes), COUNT))
    print('average/mean: %.2fms' % (1000*statistics.mean(succtimes)))
    print('standard dev: %.2fms' % (1000*statistics.stdev(succtimes)))
    print('median:       %.2fms' % (1000*statistics.median(succtimes)))
    print('\nfail: %d/%d' % (len(failtimes), COUNT))
    print('average/mean: %.2fms' % (1000*statistics.mean(failtimes)))
    print('standard dev: %.2fms' % (1000*statistics.stdev(failtimes)))
    print('median:       %.2fms' % (1000*statistics.median(failtimes)))

if __name__ == "__main__":
    main()
