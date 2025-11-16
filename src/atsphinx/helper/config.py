"""Configuration support."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from sphinx.config import Config
    from typing_extensions import Self


@dataclass
class BaseConfig:
    """Abstract class for Configuration values of your Sphinx extension.

    This is useful to implement behaviors with type annotations in your extension.

    Usage
    -----

    .. code:: python
        :title: conf.py

        # Your document configuration
        extensions = [
            "my_extension",
        ]

    .. code:: python
        :title: my_extension.py

        from dataclasses import dataclass

        from atsphinx.helper.config import BaseConfig
        from sphinx.application import Sphinx

        # Define configuration class for your extension.
        @dataclass
        class ExtensionConfig(BaseConfig):
            PREFIX = "my_"

            # Define properties that is named with removing prefix.
            my_config: str
            other: int

        def setup(app: Sphinx):
            app.add_config_value("my_config", "", "env")
            app.add_config_value("my_other_config", 1, "env")
            app.connect("html-page-context", pass_config)

        def pass_config(app, pagename, template, context, doctree):
            # Pick extension configuration as class instance.
            my_config = ExtensionConfig.make(app.config)
            # Bind instance to context. It need not bind other configuration values.
            context["my_config"] = my_config
    """

    PREFIX: ClassVar[str]
    """Prefix for configuration key."""

    @classmethod
    def from_sphinx(cls, config: Config) -> Self:
        """Create an instance of the configuration class from Sphinx cnfiguration."""
        return cls(
            **{
                field.name: getattr(config, f"{cls.PREFIX}{field.name}")
                for field in fields(cls)
            }
        )
