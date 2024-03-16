from atsphinx.helpers.decorators import only

extensions = []


@only(builders=["linkcheck"])
def setup(app):
    pass
