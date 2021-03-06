import time
import re
import sqlite3
import os
import requests
import sys

def get_followers(profile_id):
    profile_url = 'https://plus.google.com/%s/posts' % profile_id
    r = requests.get(profile_url, verify=False)

    p = re.compile(r'<h4\ class="nPQ0Mb\ pD8zNd">[\w+\ ]+\((\d+)\)')
    result = p.search(r.text)
    if result:
        if len(result.groups()) > 1:
            return
        else:
            try:
                followers = int(result.groups()[0])
                return followers
            except ValueError:
                return
    else:
        sys.stderr.write("no result whilst parsing for follower count\n")
    return




db_filename = 'profile.db'

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        #create db
        print 'Creating schema'
        conn.execute("""
        create table follower_count (
            id          integer primary key autoincrement not null,
            profile     text,
            datetime    integer,
            followers   integer)
        """)

    else:
        #don't
        print 'Database exists.  Assuming schema does too'

    profile_id = '117177689300294532641'
    followers = get_followers(profile_id)

    if followers:
        timestamp = int(time.time())
        sql = "insert into follower_count (profile, datetime, followers) values (?, ?, ?)"
        conn.execute(sql, (profile_id, timestamp, followers))
        print "inserted follower count of: %i" % followers
    else:
        sys.stderr.write("unable to fetch followers\n")