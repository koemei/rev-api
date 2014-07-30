#!/usr/bin/env python

"""
This script shows how to download docx transcripts and transform them to plain text files.
Results will be stored in /examples/transcripts/
To run this script, make sure the settings.ini file at the root of the project is properly filled.
"""

import os
import pprint
from rev.client import RevClient
from rev.models.order import Order
pp = pprint.PrettyPrinter(indent=4)

client = RevClient()

order_client_ids = [
'babc64e8-7451-4898-9477-f2c8f2495fee',
]


print "%i orders to download" % len(order_client_ids)
nb_downloaded = 0

for client_ref in order_client_ids:
    # Get the path to the transcript
    transcript_id = Order.transcript_path(
        client=client,
        client_ref=client_ref
    )
    local_file_path = "%s%s.txt" % (
        client.settings.get("base", "local_path"),
        client_ref
    )

    print "Downloading match %s -- (%i of %i)" % (transcript_id, nb_downloaded+1, len(order_client_ids))
    client.save_transcript(
        transcript_id=transcript_id,
        path=local_file_path
    )
    nb_downloaded = nb_downloaded +1

print "%i orders downloaded of %i" % (nb_downloaded, len(order_client_ids))