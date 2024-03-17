from atsphinx.helpers.decorators import setup_only

extensions = []


@setup_only(builders=["linkcheck"])
def setup(app):
    pass
