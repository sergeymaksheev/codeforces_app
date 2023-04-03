import unittest
from unittest import mock


from integration.codeforces.provider import get_result

class GetResultTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_get_result = get_result(return_value={'test':'test'})
        
    
    def test_get_result(self):
        self.assertEqual(self.mock_get_result())
