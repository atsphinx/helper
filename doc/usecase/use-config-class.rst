=============================
Use class-based configuration
=============================

Sence
=====

You are developing Sphinx extension that have some configuration values.
This extension's features use these configuration values.

You want to improve development experience using type-hints.
But :py:class:`Sphinx.config.Config` does not provide accesor for added values.

Example
=======

You can define your ``ExtensionConfig`` dataclass inherited :py:class:`BaseConfig <atsphinx.helper.config.BaseConfig>` in module.

.. code-block:: python

    from dataclasses import dataclass
    from atsphinx.helper.config import BaseConfig

    @dataclass
    class ExtensionConfig(BaseConfig):
        PREFIX = "my_"

        host: str = "localhost"
        port: int = 8080

It must be defined dataclass using :func:`dataclass <dataclasses.dataclass>`
and must add value of ``PREFIX`` as string that is used as prefix of configuration values.

Class's instance properties are used as configuration values of Sphinx.
They must be defined default value (accept ``None`` and :func:`field <dataclasses.field>`).

This class has two useful classmethods.

* :meth:`from_sphinx() <atsphinx.helper.config.BaseConfig.from_sphinx>`
  creates instance from :py:class:`Sphinx.config.Config`.
* :meth:`register() <atsphinx.helper.config.BaseConfig.register>`
  register Sphinx configuration values from class attributes.

These codes run same behavior
-----------------------------

.. code-block:: python
    :caption: Unused helper

    from sphinx.application import Sphinx
    from sphinx.config import Config

    def func(app):
       my_conf_host = app.config.my_host
       my_conf_port = app.config.my_port
       logging.info(f"host={my_conf_host}, port={my_conf_port}")

    def setup(app: Sphinx):
        app.add_config_value("my_host", "localhost", "env")
        app.add_config_value("my_port", 8080, "env")
        app.connect("builder-inited", func)

.. code-block:: python
    :caption: Used helper

    from dataclasses import dataclass
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from atsphinx.helper.config import BaseConfig

    @dataclass
    class ExtensionConfig(BaseConfig):
        PREFIX = "my_"

        host: str = "localhost"
        port: int = 8080

    def func(app):
       my_conf = ExtensionConfig.from_sphinx(app.config)
       logging.info(f"host={my_conf.host}, port={my_conf.port}")

    def setup(app: Sphinx):
        ExtensionConfig.register(app)
        app.connect("builder-inited", func)

"Used helper" is longer than "Unused helper".
But, there are two benefits.

* Defined class works overall module as type-hint.
* It can add configuration values by very simple way
