#!/usr/bin/env python
import sys
import pprint
from rev.client import RevClient
from rev.models.order_request import Input
from rev.models.order_request import TranscriptionOptions
from rev.models.order_request import OrderRequest

# usage: ./examples/orders.py

client = RevClient()
orders = client.get_orders_page().orders

for order in orders:
    print order['status']
    print order


# create input
#input = client.create_input_from_link(client.settings.get("test", "audio_test"))
#print input.__dict__

# create order
"""
inputs = [
    Input(fields={'uri': client.settings.get("test", "audio_test")}),
    Input(fields={'uri': client.settings.get("test", "audio_test")}),
    Input(fields={'uri': client.settings.get("test", "audio_test")}),
]
tc_options = TranscriptionOptions(inputs=inputs)

order_request = OrderRequest(
    fields={
        'transcription_options': tc_options,
        'client_ref': 'XB432423',
        #'comment': 'Please work quickly'
    }
)
new_order = client.submit_order(order_request=order_request)
print new_order.__dict__
"""



