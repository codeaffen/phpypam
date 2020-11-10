"""Test controller method."""
import vcr

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS


@vcr.use_cassette(cassette_name('test_controllers'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_controllers(pi):
    """Test if controllers method returns correct datatype."""
    controllers = pi.controllers()
    assert isinstance(controllers, set)
