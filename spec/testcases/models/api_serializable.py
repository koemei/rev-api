import unittest

from rev.models.api_serializable import ApiSerializable


class ApiSerializableTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        self.model = None

    def test_init(self):
        fields = {
            'field1': 'field1_value',
            'field2': 'field2_value'
        }
        self.model = ApiSerializable(fields=fields)
        assert hasattr(self.model, 'field1')
        assert self.model.field1 == fields['field1']

if __name__ == "__main__":
    unittest.main()