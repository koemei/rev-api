import unittest

from rev.client import RevClient


class RevClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = RevClient()

    def tearDown(self):
        self.client = None

    def test_get_orders_page(self):
        response = self.client.get_orders_page(page=0)
        assert hasattr(response, 'page')
        assert response.page == 0

    #def test_get_order(self):
    #    response = self.client.get_order("blabla")

    #def test_cancel_order(self):
    #    response = self.client.cancel_order("blabla")

    def test_create_input_from_link(self):
        response = self.client.create_input_from_link(self.client.settings.get("test", "audio_test"))
        assert response.status_code == 201