"""Helpful decorators."""

import functools
import logging
from typing import Any, Callable, List, Optional, Union

from sphinx.application import Sphinx
from sphinx.util.logging import getLogger

Logger = getLogger(__name__)


def setup_only(
    *,
    builders: Optional[List[str]] = None,
    formats: Optional[List[str]] = None,
    loglevel: int = logging.WARN,
):
    """Restict extension workings by builder types or formats.

    This is decorator function for setup of extension.
    You can message for users that this extension is created for specify builders.

    .. code-block:: python
       :caption: your_extension.py
       :name: your_extension.py

       # Display warning when user runs by not 'html' builders.
       @setup_only(builder=["html"])
       def setup(app):
           ...

    :params builders: List of builder names for restrict target.
    :params formats: List of format types for restrict target.
    :params loglevel: Level about logger of wrapper function.
    """
    if builders is None and formats is None:
        Logger.log(
            loglevel,
            "To use @only, you should set argument builders or formats at least.",
        )

    def _only(func: Callable[[Sphinx], Union[dict, None]]):
        logger = getLogger(func.__module__ or "confpy")

        def _restrict_builder(app: Sphinx):
            target = func.__module__ or "setup() on conf.py"
            if builders and app.builder.name not in builders:
                logger.log(
                    loglevel, f"{target} is not supported '{app.builder.name}' builder."
                )
            if formats and app.builder.format not in formats:
                logger.log(
                    loglevel,
                    f"{target} is not supported '{app.builder.format}' format.",
                )

        @functools.wraps(func)
        def __only(app: Sphinx) -> Optional[dict]:
            app.connect("builder-inited", _restrict_builder)
            return func(app)

        return __only

    return _only


def emit_only(
    *,
    builders: Optional[List[str]] = None,
    formats: Optional[List[str]] = None,
    loglevel: int = logging.INFO,
    return_alt: Any = None,
):
    """Restict event handler workings by builder types or formats.

    This is decorator function for core-event handler of extension.
    You can skip procedure of extension when builder or format is not specify types.

    .. code-block:: python
       :caption: your_extension.py
       :name: your_extension.py

       # Proc does not run when user runs by not 'html' builders.
       @emit_only(builder=["html"])
       def event_handler(app):
           ...


       def setup(app):
           app.connect("builder-inited", event_handler)
           ...

    :params builders: List of builder names for restrict target.
    :params formats: List of format types for restrict target.
    :params loglevel: Level about logger of wrapper function.
    :params return_alt: Return value if guard is worked.
    """
    if builders is None and formats is None:
        Logger.log(
            loglevel,
            "To use @emit_only, you should set argument builders or formats at least.",
        )

    def _only(func: Callable[[Sphinx, ...], Any]):
        logger = getLogger(func.__module__ or "confpy")

        @functools.wraps(func)
        def __only(app: Sphinx, *args, **kwargs) -> Any:
            if builders and app.builder.name not in builders:
                logger.log(
                    loglevel,
                    f"{func.__name__} is not supported '{app.builder.name}' builder.",
                )
                return return_alt
            if formats and app.builder.format not in formats:
                logger.log(
                    loglevel,
                    f"{func.__name__} is not supported '{app.builder.format}' format.",
                )
                return return_alt
            return func(app, *args, **kwargs)

        return __only

    return _only
