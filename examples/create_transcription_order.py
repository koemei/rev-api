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
    # (<path to the media file>, <duration of the media file>)
    (client.settings.get("test", "audio_test"), client.settings.get("test", "audio_test_duration"))
]

# convert the media list to an input list
inputs = []
for url, length in media:
    inputs.append(
        Input(fields={
            'uri': url,
            'audio_length': length
        })
    )
tc_options = TranscriptionOptions(inputs=inputs)

# create the order request
order_request = OrderRequest(
    fields={
        'transcription_options': tc_options,
        'client_ref': client.settings.get("test", "order_reference"),
        #'notification': Notification(url=client.settings.get("test", "notification_url"))
        #'comment': 'Extra bacon!'
    }
)
new_order = client.submit_order(order_request=order_request)
print new_order.__dict__