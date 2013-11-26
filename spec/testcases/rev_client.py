import unittest
import math

from rev.client import RevClient


class RevClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = RevClient()

    def tearDown(self):
        self.client = None

    def test_get_orders_page(self):
        # Test first page
        first_page = self.client.get_orders_page(page=0)
        assert hasattr(first_page, 'page')
        assert first_page.page == 0

        if first_page.total_count > 0:
            assert len(first_page.orders) > 0

            # Test last page
            last_page_number = int(math.ceil(first_page.total_count/first_page.results_per_page))
            last_page = self.client.get_orders_page(page=last_page_number)
            assert last_page.page == last_page_number
            assert len(last_page.orders) > 0
            assert len(last_page.orders) == first_page.results_per_page - (first_page.results_per_page * (last_page_number+1)) + first_page.total_count

            # Test no more pages
            unexisting_page = self.client.get_orders_page(page=last_page_number+1)
            assert unexisting_page.page == last_page_number+1
            assert len(unexisting_page.orders) == 0

    #def test_get_order(self):
    #    response = self.client.get_order("blabla")

    #def test_cancel_order(self):
    #    response = self.client.cancel_order("blabla")

    def test_create_input_from_link(self):
        response = self.client.create_input_from_link(self.client.settings.get("test", "audio_test"))
        assert response.status_code == 201