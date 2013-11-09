from rev.models.api_serializable import ApiSerializable


class OrderRequest(ApiSerializable):
    """
    OrderRequest is used for constructing order 'spec' in consumer code and passing it into.
    It consists of three main elements: :payment, :transcription_options and :notification.
    You can also supply reference number and customer comment

    @note http://www.rev.com/api/ordersposttranscription, http://www.rev.com/api/ordersposttranslation
    """

    def __json__(self):
        return {
            'payment': self.payment.__json__(),
            'transcription_options': self.transcription_options.__json__(),
            'client_ref': self.client_ref
        }

    def __init__(self, fields, payment=None):
        """
        @param payment [Payment] payment info
        @param fields [Hash] of fields to initialize instance. See instance attributes for available fields.
        """
        super(OrderRequest, self).__init__(fields)
        if payment is None:
            payment = Payment()
        self.payment = payment


class Payment(ApiSerializable):
    """
    Payment Info. Payment can be done either by charging a credit card or by debiting the user's
    account balance. If using a credit card, then either the user's saved credit card can be used
    or credit card details provided.

    For credit card payments, if specifying the credit card details in the request, the required
    elements are the card number, cardholder name, expiration month and year, and billing zipcode.
    If using the user's saved card, you must currently specify the value "1" for the saved card id,
    as we currently only allow a single card to be saved for a user.
    """

    # use to correctly set payment type
    TYPES = {
        'credit_card': 'CreditCard',
        'balance': 'AccountBalance'
    }

    def __json__(self):
        return {
            'type': self.type,
        }


    CC_ON_FILE_ID = 1

    def __init__(self, type=None, credit_card=None):
        """
        @param type [String] payment method
        @param credit_card [CreditCard] cc obj, if type is 'CreditCard'
        """
        super(Payment, self).__init__(fields=None)
        if type is None:
            type = self.TYPES['balance']
        self.type = type
        self.credit_card = credit_card


class BillingAddress(ApiSerializable):
    pass


class CreditCard(ApiSerializable):
    pass


class TranscriptionOptions(ApiSerializable):
    """
    Transcription options. This section contains the input media that must be transferred to our servers
    using a POST to /inputs, and are referenced using the URIs returned by that call. We also support external links.
    Following points explain usage of inputs:
    - For each input, you must provide either uri or external_link, but not both. If both or neither is provided,
    error is returned.
    - You should only provide an external_link if it links to page where the media can be found, rather than directly to
    the media file, and that we will not attempt to do anything with the link when the API call is made.
    This is in contrast to when you post to /inputs with a link to a media file - in that case we do download the file.
    So the external_link should only be used when you can't link to the media file directly.
    - The external_link can contain anything you want, but if it's a YouTube link, we will attempt to determine the
    duration of the video on that page.
    We also allow users of the api to specify if translation should be done using our Verbatim option (:verbatim => true)
    and to specify if Time stamps should be included (:timestamps => true).
    """

    def __json__(self):
        return {
            'inputs': [input.__json__() for input in self.inputs],
        }


    def __init__(self, inputs, fields=None):
        """
        @param inputs [Array] list of inputs
        @param info [Hash] of fields to initialize instance. May contain:
        - :verbatim => true/false
        - :timestams => true/false
        """
        super(TranscriptionOptions, self).__init__(fields=fields)
        self.inputs = inputs


class Input(ApiSerializable):
    """
    Input for order (aka source file)
    """
    def __json__(self):
        return {
            'external_link': self.uri,
            'audio_length': self.audio_length
        }


class Notification(ApiSerializable):
    """
    Notification Info. Optionally you may request that an HTTP post be made to a url of your choice when the order enters
    a new status (eg being transcribed or reviewed) and when it is complete.
    """

    # Notification levels
    LEVELS = {
      'detailed': 'Detailed',
      'final_only': 'FinalOnly'
    }

    def __init__(self, url, level=None):
        """
        @param url [String] The url for notifications. Mandatory if the notifications element is used. Updates will be posted to this URL
        @param level [String] Optional, specifies which notifications are sent:
        - :detailed - a notification is sent whenever the order is in a new status or has a new comment
        - :final_only - (the default), notification is sent only when the order is complete
        """
        super(Notification, self).__init__(fields=None)
        self.url = url
        self.level = level if level is not None else self.LEVELS['final_only']