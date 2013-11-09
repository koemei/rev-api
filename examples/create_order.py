#!/usr/bin/env python

import pprint
from rev.client import RevClient
from rev.models.order_request import Input
from rev.models.order_request import TranscriptionOptions
from rev.models.order_request import OrderRequest
from rev.models.order_request import Notification
pp = pprint.PrettyPrinter(indent=4)

client = RevClient()

media = [
    ('path_to_the_media_file',15)
]

inputs = []
for url, length in media:
    inputs.append(
        Input(fields={
            'uri': url,
            'audio_length': length
        })
    )

tc_options = TranscriptionOptions(inputs=inputs)
order_request = OrderRequest(
    fields={
        'transcription_options': tc_options,
        'client_ref': 'BK-CS169-w7-8',
        #'notification': Notification(url='<https://www.yoursite.com/callback_endpoint>')
        #'comment': 'Extra bacon'
    }
)
new_order = client.submit_order(order_request=order_request)
print new_order.__dict__