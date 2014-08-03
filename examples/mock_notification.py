"""
Mock rev notifications
"""

import os
import pprint
from rev.client import RevClient
from rev.models.order import Order
pp = pprint.PrettyPrinter(indent=4)

client = RevClient()

order_client_ids = [
    """
    List of TSP processes
    <process_tsp.uuid>,
    <process_tsp.uuid>,
    ...,
    """
]


print "%i notifications to do" % len(order_client_ids)

for client_ref in order_client_ids:
    order_number = Order.get_ref_from_client_ref(client=client, client_ref=client_ref)
    Order.mock_notification(order_number=order_number, client_ref=client_ref)