"""Standard integration tests."""

from io import StringIO

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__print_warning(app: SphinxTestApp, warning: StringIO):
    app.build()
    expected = "is not supported 'html' builder."
    assert expected in warning.getvalue()
