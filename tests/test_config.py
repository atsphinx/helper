from dataclasses import dataclass

import pytest
from atsphinx.helper import config as tst
from sphinx.testing.util import SphinxTestApp


def setup(app):
    app.add_config_value("demo_host", "localhost", "env")
    app.add_config_value("demo_port", 8080, "env")


@dataclass
class _DemoConfig(tst.BaseConfig):
    PREFIX = "demo_"

    host: str
    port: int


@pytest.mark.sphinx("html", testroot="with-conf")
def test_demo_config_from_sphinx(app: SphinxTestApp):
    config = _DemoConfig.make(app.config)
    assert config.host == "localhost"
    assert config.port == 8000
