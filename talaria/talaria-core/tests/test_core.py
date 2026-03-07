"""Tests for talaria-core."""


def test_version():
    """Test version is defined."""
    import talaria

    assert talaria.__version__ == "0.1.0"


def test_namespace_import():
    """Test namespace package works."""
    import talaria

    assert hasattr(talaria, "__version__")
