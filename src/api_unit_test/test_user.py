# Standard library imports...
from unittest import skipIf
from unittest.mock import Mock, patch

# Third-party imports...
from nose.tools import assert_is_none, assert_true
# Local imports...
import sys
sys.path.append('../api/')
from user import api_user_group

class TestUser(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('user.api_user_group')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_getting_api_user_group_when_response_is_ok(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = Mock()
        self.mock_get.return_value= "{}"
        
        # Call the service, which will send a request to the server.
        response = api_user_group()

        print (response)
        # If the request is sent successfully, then I expect a response to be returned.
        assert_true(response, self.mock_get.return_value)
