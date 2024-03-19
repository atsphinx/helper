from atsphinx.helper.decorators import emit_only
from sphinx.util.logging import getLogger

extensions = []


@emit_only(builders=["linkcheck"])
def event_handler(app):
    getLogger("test").warning("Message is not displayed on html builder.")


def setup(app):
    app.connect("builder-inited", event_handler)
