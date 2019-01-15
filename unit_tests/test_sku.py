'''Unit testing module'''
import unittest2 as unittest
from api_manager.core.sku import get_sku_by_filters
import httplib
from rest_framework import request
from mock import patch


class TestSKU(unittest.TestCase):
    """
    @summary: A Class to test sku functionality
    """

    @classmethod
    def setUpClass(self):
        """
        @summary: A setup class
        """
        self.exception = "Input parameter missing for the api: " \
                         "department,category,location,subcategory"

    def setUp(self):
        """
        @summary: A setup function
        """
        self.req = request.Request

    def tearDown(self):
        """
        @summary: A tear down function
        """
        self.req.query_params = None

    def test_get_sku_by_filters_invalid_param(self):
        """
        @summary: Unit test for sku api with invalid parameters
        """
        self.req.query_params = {'param': 'value'}
        response = get_sku_by_filters(self.req)
        assert response.status_code == httplib.BAD_REQUEST

    @patch('api_manager.core.sku.SubCategorySerializer')
    def test_get_sku_by_filters_with_side_effects(self, mock_serializer):
        """
        @summary: Unit test for sku api with exception
        """
        self.req.data = {"location": "Perimeter", "department": "Bakery",
                         "category": "Bakery Bread", "subcategory": "Bagels"}
        mock_serializer.side_effect = Exception("Some error")
        response = get_sku_by_filters(self.req)
        assert response.status_code == httplib.INTERNAL_SERVER_ERROR

    def test_get_sku_by_filters_with_success(self):
        """
        @summary: Unit test for sku api with success
        """
        self.req.data = {"location": "Perimeter", "department": "Bakery",
                         "category": "Bakery Bread", "subcategory": "Bagels"}
        response = get_sku_by_filters(self.req)
        assert response.status_code == httplib.OK


if __name__ == "__main__":
    unittest.main()
