"""Configuration support."""

from __future__ import annotations

import logging
from dataclasses import _MISSING_TYPE, dataclass, fields
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from sphinx.application import Sphinx
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
            host: str
            port: int

        def setup(app: Sphinx):
            ExtensionConfig.register(app)
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

    @classmethod
    def register(cls, app: Sphinx) -> None:
        """Register fields as Sphinx configuration values.

        This method is useful to manage exention configuration by only class itself.

        .. todo:: This does not support 'description' of newer Sphinx.
        """
        for field in fields(cls):
            # Resolve 'default' argument
            default_value = field.default
            if not isinstance(field.default, _MISSING_TYPE):
                pass
            elif isinstance(field.default_factory, _MISSING_TYPE):
                default_value = None
            else:
                default_value = field.default_factory()
            # Resolve 'rebuild' argument
            rebuild_value = "env"
            if "sphinx_rebuild" in field.metadata:
                value = field.metadata["sphinx_rebuild"]
                if isinstance(value, bool) or isinstance(value, str):
                    rebuild_value = value
                else:
                    logging.warning(
                        f"'sphinx_rebuild' only supports bool or str: {type(value)}"
                    )
            app.add_config_value(
                cls.PREFIX + field.name, default_value, rebuild_value, field.type
            )
