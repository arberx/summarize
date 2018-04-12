"""
package initializer.

Credit: Arber Xhindoli
"""
import os
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

import summarize.views  # noqa: E402  pylint: disable=wrong-import-position
