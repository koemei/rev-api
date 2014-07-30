#!/usr/bin/env python

"""
This script shows how to create a transcription order.
To run this script, make sure the settings.ini file at the root of the project is properly filled.
"""


import pprint
from rev.client import RevClient
from rev.models.order_request import Input
from rev.models.order_request import TranscriptionOptions
from rev.models.order_request import OrderRequest
from rev.models.order_request import Notification
pp = pprint.PrettyPrinter(indent=4)

client = RevClient()

# list of media items to transcribe
media = [
    # (<client_order_reference>, <path to the media file>, <duration of the media file>, <filename>)
    #(
    #    client.settings.get("test", "order_reference"),
    #    client.settings.get("test", "audio_test"),
    #    client.settings.get("test", "audio_test_duration"),
    #    client.settings.get("test", "filename"),
    #)
('babc64e8-7451-4898-9477-f2c8f2495fee','https://usermedia.koemei.com.s3.amazonaws.com/d5cf61db-cb7b-452b-b046-893c3e7efdc8/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/14-07-23/d2aeec07-1e7b-4309-8ff5-d9f9ff8411c5/babc64e8-7451-4898-9477-f2c8f2495fee.mp4?Signature=FIE7LSUASqNrqbvQb%2FviDicig9A%3D&Expires=1406550750&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA',3, 'UNEX-X477.1/x477_1_m5_ s1.mp4'),
]

# convert the media list to an input list
for ref, url, length, filename in media:
    inputs = [
        Input(fields={
            'uri': url,
            'audio_length': length,
            'filename': filename
        })
    ]
    tc_options = TranscriptionOptions(inputs=inputs)

    # create the order request
    order_request = OrderRequest(
        fields={
            'transcription_options': tc_options,
            'client_ref': ref,
            'notification': Notification(url=client.settings.get("base", "paths.koemei.callback")),
            'comment': 'Please do not indicate speaker names in the text.'
        }
    )
    new_order = client.submit_order(order_request=order_request)
    print "Created new order"
    print new_order.__dict__

print "Created new order (%i files, %i minutes)" % (len(media), sum([duration[2] for duration in media]))
