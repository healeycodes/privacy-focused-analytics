import sys
import sqlite3
DB = 'analytics.db'

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER,
    path TEXT,
    title TEXT,
    referrer TEXT,
    country TEXT,
    device TEXT,
    width INTEGER, 
    height INTEGER
    )''')
conn.commit()
conn.close()


def save(timestamp=0, path='', title='', referrer='', country='', device='', width=0, height=0):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    statement = '''INSERT INTO data (
        timestamp,
        path,
        title,
        referrer,
        country,
        device,
        width,
        height
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    c.execute(statement, [timestamp, path, title,
                          referrer, country, device, width, height])
    conn.commit()
    conn.close()


def load(start=0, end=sys.maxsize):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        '''SELECT * FROM data WHERE timestamp >= ? and timestamp < ?''', [start, end])
    result = [dict(row) for row in c.fetchall()]
    conn.close()
    return result
