"""
xblock helpers.
"""
import os
from html.parser import HTMLParser

import openai
from openai.error import OpenAIError
from django.template import Context, Engine

html_parser = HTMLParser()  # pylint: disable=invalid-name


def render_template(template_name, **context):
    """
    Render static resource using provided context.

    Returns: django.utils.safestring.SafeText
    """
    template_dirs = [os.path.join(os.path.dirname(__file__), "static/html")]
    libraries = {"chatgpt_tags": "chatgpt.templatetags"}
    engine = Engine(dirs=template_dirs, debug=True, libraries=libraries)
    html = engine.get_template(template_name)

    return html_parser.unescape(html.render(Context(context)))


def validate_openai_key(key):
    openai.api_key = key
    try:
        openai.Completion.create(engine="text-davinci-002", prompt="A", max_tokens=3)
        return True
    except OpenAIError:
        return False
