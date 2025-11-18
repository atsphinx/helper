======================================
Only works features sepecified builder
======================================

Scene
=====

You are developing Sphinx extension to work as event handler for only specified builder.
This extension mutate doctree in writing phase, and this requires long time for process.

You want to skip this process when running by other builders
if builder need not this, because this mutation is required for only specified builder.

Example
=======

You can decorate event handler with :py:func:`atsphinx.helper.decorators.emit_only` to restrict event emit to specified builder.

.. code-block:: python
    :caption: your_extension.py

    from atsphinx.helper.decorators import emit_only

    @emit_only(builders=["html"])
    def process_doctree(app, doctree):
        # Your code here

    def setup(app):
        app.connect("doctree-resolved", process_doctree)

When function is  decorated with ``["html"]`` kwargs, it works only if builder name is "html".
When other builder runs, it is skipped with output message into console.

If you set ``formats=["html"]``, it works only if application runs with all builders that are set ``format`` is "html".
This is useful when you want to work for html output.
