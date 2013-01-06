#!/usr/bin/env python

import httplib
conn = httplib.HTTPConnection("api.glitch.com")
conn.request("GET", '/simple/auctions.list?per_page=1000&defs=1')
r1 = conn.getresponse()
json_from_server = r1.read()
conn.close()



import MySQLdb
db=MySQLdb.connect(db="ecurnomics", user="ecurnomics_user", passwd="iekeeyegoagheezi")
db.autocommit(False)
c = db.cursor()


import json
import datetime
data = json.loads(json_from_server)
#data = json.loads(open("auctions.list").read())

#print data['items'].keys()

for auction_code in data['items'].keys():
    auction = data['items'][auction_code]
    cost = float(auction['cost'])
    count = int(auction['count'])
    player_tsid = auction['player']['tsid']
    player_name = auction['player']['name'].encode('utf-8')
    unit_cost = cost / count
    class_tsid = auction['class_tsid']
    category = auction['category']
    created = auction['created']
    datetime_created = datetime.datetime.fromtimestamp(float(created))
    created_milliseconds = int(created)*1000
    expires = auction['expires']
    url = auction['url']

    # Pretty item details
    item_def = auction['item_def']
    name_single = item_def['name_single']
    name_plural = item_def['name_plural']
    max_stack = item_def['max_stack']
    desc = item_def['desc']
    base_cost = item_def['base_cost']
    iconic_url = item_def['iconic_url']
    swf_url = item_def['swf_url']

    # Catch crazy unicode chars
    charmap = {
        0x2026: u"...", # Translate ellipsis char to three dots
        0x2019: u"'", # Translate apostrophe
        0x2013: u"-", # Translate En Dash
        0x2014: u"-", # Translate Em Dash
        0x2018: u"'", # Translate Back qoute
    }
    desc = desc.translate(charmap)

    c.execute("""
        replace into ecurnomics_auction (auction_code, class_tsid, cost, count, player_tsid, player_name, unit_cost, category, created, datetime_created, created_milliseconds, expires, url)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
              [auction_code, class_tsid, cost, count, player_tsid, player_name, unit_cost, category, created, datetime_created, created_milliseconds, expires, url]
    )

    c.execute("""
        replace into ecurnomics_item (class_tsid, name_single, name_plural, max_stack, description, base_cost, iconic_url, swf_url, category)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
              [class_tsid, name_single, name_plural, max_stack, desc, base_cost, iconic_url, swf_url, category]
    )

db.commit()
