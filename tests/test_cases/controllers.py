"""Test controller method."""


def test_controllers(pi):
    """Test if controllers method returns correct datatype."""
    controllers = pi.controllers()
    assert isinstance(controllers, set)
