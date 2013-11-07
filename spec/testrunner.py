import unittest

from spec.testcases.base_client import BaseClientTestCase
from spec.testcases.rev_client import RevClientTestCase
from spec.testcases.models.api_serializable import ApiSerializableTestCase

suite = unittest.TestLoader().loadTestsFromTestCase(BaseClientTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(RevClientTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(ApiSerializableTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)