"""Standard integration tests."""

from io import StringIO

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__print_warning(app: SphinxTestApp, warning: StringIO):
    app.build()
    expected = "is not supported 'html' builder."
    assert expected in warning.getvalue()


@pytest.mark.sphinx("html", testroot="emit")
def test__skip_by_emit(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    "is not supported 'html' builder." in status.getvalue()
    "Message is not displayed on html builder." not in warning.getvalue()
