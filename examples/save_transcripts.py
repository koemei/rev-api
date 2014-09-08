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
    ('c865eb7a-1f82-4fb4-844f-e0946b4e6c33', 'TC0004567767')
]


print "%i orders to download" % len(order_client_ids)
nb_downloaded = 0

for client_ref, order_number in order_client_ids:
    # Get the path to the transcript
    transcript_id = Order.transcript_path(
        client=client,
        client_ref=client_ref,
        order_number=order_number
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
