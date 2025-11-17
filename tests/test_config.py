from dataclasses import dataclass, field, make_dataclass
from typing import Any, Union
from unittest import mock

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
    config = _DemoConfig.from_sphinx(app.config)
    assert config.host == "localhost"
    assert config.port == 8000


@pytest.mark.parametrize(
    "fields,expected_items",
    [
        (
            [("host", str, "localhost")],
            [("test_host", "localhost", "env", str)],
        ),
        (
            [("host", str, field(default="localhost"))],
            [("test_host", "localhost", "env", str)],
        ),
        (
            [
                (
                    "host",
                    str,
                    field(default="localhost", metadata={"sphinx_rebuild": "html"}),
                )
            ],
            [("test_host", "localhost", "html", str)],
        ),
        (
            [("host", Union[str, None], None)],
            [("test_host", None, "env", Union[str, None])],
        ),
        (
            [("port", int, 8080)],
            [("test_port", 8080, "env", int)],
        ),
        (
            [("hosts", list[str], field(default_factory=list))],
            [("test_hosts", [], "env", list[str])],
        ),
        (
            [("options", dict, field(default_factory=dict))],
            [("test_options", {}, "env", dict)],
        ),
        (
            [("host", str, "localhost"), ("port", int, 8080)],
            [
                ("test_host", "localhost", "env", str),
                ("test_port", 8080, "env", int),
            ],
        ),
    ],
)
def test_BaseConfig__register(
    fields: list[tuple[str, type, Any]], expected_items: list[tuple]
):
    class BaseConfig(tst.BaseConfig):
        PREFIX = "test_"

    Config = make_dataclass("Config", fields=fields, bases=(BaseConfig,))
    app = mock.MagicMock()
    Config.register(app)  # type: ignore[unresolved-attribute]
    assert app.add_config_value.call_count == len(expected_items)
    for idx, expected in enumerate(expected_items):
        assert app.add_config_value.call_args_list[idx].args == expected
