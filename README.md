Rev API python client
==================================

Description
------------
This module give access to the Rev API, and lets you create orders and track them.
See API documentation: http://www.rev.com/api

Installation
------------

1 Install :
```
python setup.py install
```
2 Copy settings.example.ini to settings.ini and fill in your credentials and configuration options.

Usage
--------

```
python
>>> from rev.client import RevClient
>>> client = RevClient()
>>> client.prepay_balance()
u'1.00'
>>> client.order_url("http://example.com/media.mp3")
{u'message': u"Order '0a0' Created", u'audiofiles': [0000001], u'order': u'0a0'}
```

or

```
python ex/order_mediaid.py
```

Known issues
---------

Soon...

Troubleshooting
----------

Soon also!

Next steps
----------

TBD

Questions
----------

TBD