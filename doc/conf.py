from atsphinx.helper import __version__

# -- Project information -----------------------------------------------------
project = "atsphinx-helper"
copyright = "2024, Kazuya Takei"
author = "Kazuya Takei"
release = __version__

# -- General configuration ---------------------------------------------------
extensions = [
    # Bundled extensions
    "sphinx.ext.autodoc",
    # Third-party extensions
    "myst_parser",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_title = f"{project} v{release}"
