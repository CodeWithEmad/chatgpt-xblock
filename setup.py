"""Setup for ChatGPT XBlock."""
import os
import re

from setuptools import setup


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)

    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def package_data(pkg, roots):
    """
    Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.
    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


VERSION = get_version("chatgpt", "__init__.py")
DESCRIPTION = "edSPIRIT AI Assistant XBlock"

setup(
    name="chatgpt-xblock",
    version=VERSION,
    description=DESCRIPTION,
    license="AGPL v3",
    packages=[
        "chatgpt",
    ],
    install_requires=[
        "XBlock==1.6.2",
        "openai==0.28.1",
    ],
    entry_points={
        "xblock.v1": [
            "chatgpt = chatgpt:ChatGPTXBlock",
        ]
    },
    package_data=package_data(
        "chatgpt", ["static", "public", "locale", "translations"]
    ),
)
