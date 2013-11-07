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
        @return [OrdersListPage] paged result cointaining 'orders'
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
        print response
        return response

    def dl_transcripts(self, order):
        pass
        #if order.transcripts.empty?
        #puts "There are no transcripts for order #{order_num}"
        #return
        #filenames = order.transcripts.map { |t| t.name}.join(',')
        #puts "Downloading files: #{filenames}"
        #order.transcripts.each do |t|
        #  @rev_client.save_attachment_content t.id, t.name
