import os
import pprint
from rev.client import RevClient
from rev.utils import docx_to_txt
pp = pprint.PrettyPrinter(indent=4)

client = RevClient()
orders = client.get_orders_page().orders
for order in orders:
    #pp.pprint(order)
    if order['status'] == 'Complete' and order['order_number'] == 'TC1026737301':
        for att in order['attachments']:
            if att['kind'] == 'transcript':
                docx_dest = "examples/transcripts/docx/%s" % att["name"].split('.')[0]+".docx"
                if not os.path.exists(docx_dest):
                    client.save_transcript(
                        transcript_id=att["id"],
                        path=docx_dest
                    )
                    txt_dest = "examples/transcripts/txt/%s" % att["name"].split('.')[0]+".txt"
                    docx_to_txt(source=docx_dest, dest=txt_dest)
                else:
                    print "skip %s, already present" % docx_dest