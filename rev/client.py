from rev.base_client import BaseClient

from rev.models.order import OrderListPage
from rev.models.order import Order


class RevClient(BaseClient):
    """
    Access to the Rev API.  Order transcripts, and track their progress
    """

    def __init__(self):
        """
        Create the api client
        """
        super(RevClient, self).__init__()

    def get_orders_page(self, page=0):
        """
        Loads single page of existing orders for current client
        @note http://www.rev.com/api/ordersget
        @param page [Int, nil] 0-based page number, defaults to 0
        @return [OrdersListPage] paged result containing 'orders'
        """
        response = self.request_get(
            url=["orders"],
            params={
                'page': page
            }
        )
        return OrderListPage(fields=response)

    def get_all_orders(self):
        """
        Loads all orders for current client. Works by calling get_orders_page multiple times.
        Use with caution if your order list might be large.
        @note http://www.rev.com/api/ordersget
        @return [Array of Order] list of orders
        """
        raise NotImplementedError()

    def get_order(self, number):
        """
        Returns Order given an order number.
        @note http://www.rev.com/api/ordersgetone
        @param number [String] order number, like 'TCXXXXXXXX'
        @return [Order] order obj
        """
        response = self.request_get(
            url=["orders", number]
        )
        return Order(fields=response)

    def create_input_from_link(self, url, filename=None, content_type=None):
        """
        Request creation of a source input based on an external URL which the server will attempt to download.
        @note http://www.rev.com/api/inputspost

        @param url [String] mandatory, URL where the media can be retrieved. Must be publicly accessible.
        HTTPS urls are ok as long as the site in question has a valid certificate
        @param filename [String, nil] optional, the filename for the media. If not specified, we will
        determine it from the URL
        @param content_type [String, nil] optional, the content type of the media to be retrieved.
        If not specified, we will try to determine it from the server response
        @return [String] URI identifying newly uploaded media. This URI can be used to identify the input
        when constructing a OrderRequest object to submit an order.
        {Rev::BadRequestError} is raised on failure (.code attr exposes API error code -
        see {Rev::InputRequestError}).
        """
        response = self.request_post(
            url=['inputs'],
            params={
                'url': url
            }
        )
        return response

    def submit_order(self, order_request):
        """
        Submit a new order using {Rev::OrderRequest}.
        @note http://www.rev.com/api/ordersposttranscription - for full information

        @param order_request [OrderRequest] object specifying payment, inputs, options and notification info.
        inputs must previously be uploaded using upload_input or create_input_from_link
        @return [String] order number for the new order
        Raises {Rev::BadRequestError} on failure (.code attr exposes API error code -
        see {Rev::OrderRequestError}).
        """
        response = self.request_post(
            url=['orders'],
            params=order_request.__json__()
        )
        return response

    def save_transcript(self, transcript_id, path):
        """
        Get the raw data for the attachment with given id.
        Download the contents of an attachment and save it into a file. Use this method to download either a finished transcript,
        finished translation or a source file for an order.
        For transcript and translation attachments, you may request to get the contents in a specific
        representation, specified via a mime-type.

        See {Rev::Order::Attachment::REPRESENTATIONS} hash, which contains symbols for currently supported mime types.
        The authoritative list is in the API documentation at http://www.rev.com/api/attachmentsgetcontent

        @param transcript_id [String] rev id of the transcript to save.
        @param path [String] path to file into which the content is to be saved.
        @param mime_type [String, nil] mime-type for the desired format in which the content should be retrieved.
        @return [String] filepath content has been saved to. Might raise standard IO exception if file creation files
        """

        response = self.request_get(
            url=["attachments", transcript_id, "content"],
            headers={
                'Accept': 'text/plain',
                'Accept-Charset': 'iso-8859-1'
            },
            stream=True
        )
        with open(path, "wb") as local_file:
            try:
                local_file.write(response.content)
            except Exception, e:
                self.log.error("Error saving transcript %s to %s" % (transcript_id, path))
                self.log.error(e)
                raise