#!/usr/bin/env python

"""
This script shows how to download docx transcripts and transform them to plain text files.
Results will be stored in /examples/transcripts/
To run this script, make sure the settings.ini file at the root of the project is properly filled.
"""

import os
import pprint
from rev.client import RevClient
pp = pprint.PrettyPrinter(indent=4)

order_number = '<fill in the order number from which to download>'

client = RevClient()
orders = client.get_orders_page().orders
for order in orders:
    #pp.pprint(order)
    if order['order_number'] == order_number:
        for att in order['attachments']:
            if att['kind'] == 'transcript':
                print att["name"]
                local_file_path =  "%s%s" % (
                    client.settings.get("test", "local_path"),
                    att["name"].replace('.docx','').replace('.mp4','')+".txt"
                )
                if not os.path.exists(local_file_path):
                    try:
                        client.save_transcript(
                            transcript_id=att["id"],
                            path=local_file_path
                        )
                    except Exception, e:
                        print "Error downloading transcript for %s" % att["name"]