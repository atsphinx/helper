"""Helpful decorators."""

import functools
from typing import Callable, List, Optional, Union

from sphinx.application import Sphinx
from sphinx.util.logging import getLogger

Logger = getLogger(__name__)


def only(*, builders: Optional[List[str]] = None, formats: Optional[List[str]] = None):
    """Restict extension by builder types or formats.

    This is decorator function.
    You can message for users that this extension is created for specify builders.

    .. code-block:: python
       :caption: your_extension.py
       :name: your_extension.py

       # Display warning when user runs by not 'html' builders.
       @only(builder=["html"])
       def setup(app):
           ...

    :params builders: List of builder names for restrict target.
    :params formats: List of format types for restrict target.
    """
    if builders is None and formats is None:
        Logger.warning(
            "To use @only, you should set argument builders or formats at least."
        )

    def _only(func: Callable[[Sphinx], Union[dict, None]]):
        logger = getLogger(func.__module__ or "confpy")

        def _restrict_builder(app: Sphinx):
            target = func.__module__ or "setup() on conf.py"
            if builders and app.builder.name not in builders:
                logger.warning(
                    f"{target} is not supported '{app.builder.name}' builder."
                )
            if formats and app.builder.format not in formats:
                logger.warning(
                    f"{target} is not supported '{app.builder.format}' format."
                )

        @functools.wraps(func)
        def __only(app: Sphinx):
            app.connect("builder-inited", _restrict_builder)
            func(app)

        return __only

    return _only
