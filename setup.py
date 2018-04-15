""" summarize python package configuration."""

from setuptools import setup

setup(
    name='summarize',
    version='0.1.0',
    packages=['summarize'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'urllib3',
        'Werkzeug',
        'Jinja2',
        'gunicorn',
        'click'
    ],
)
