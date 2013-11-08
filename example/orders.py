#!/usr/bin/env python
import sys
import pprint
from rev.client import RevClient
from rev.models.order_request import Input
from rev.models.order_request import TranscriptionOptions
from rev.models.order_request import OrderRequest
from rev.models.order_request import Notification

# usage: ./examples/orders.py

client = RevClient()
orders = client.get_orders_page().orders

for order in orders:
    print order['status']
    print order
    if order['status'] == 'Complete':
        for att in order['attachments']:
            print att["id"]
            #client.save_transcript(transcript_id=order['attachments'][0]["id"], path="%s.txt"%order['attachments'][0]["id"])

# create input
#input = client.create_input_from_link(client.settings.get("test", "audio_test"))
#print input.__dict__

# create order
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
        'client_ref': '<OrderReference>',
        #'notification': Notification(url='<https://www.yoursite.com/callback_endpoint>')
        #'comment': 'Extra bacon'
    }
)
new_order = client.submit_order(order_request=order_request)
print new_order.__dict__
