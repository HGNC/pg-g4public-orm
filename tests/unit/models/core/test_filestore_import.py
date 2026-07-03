import pytest

def test_filestore_model_exists():
    """Test that will fail until the Filestore model exists."""
    try:
        from pg_g4public_orm.models.core.filestore import Filestore
        assert Filestore is not None
    except ImportError:
        pytest.fail("Filestore model not implemented yet")

def test_import_model_exists():
    """Test that will fail until the Import model exists."""
    try:
        from pg_g4public_orm.models.core.import_model import Import
        assert Import is not None
    except ImportError:
        pytest.fail("Import model not implemented yet")
