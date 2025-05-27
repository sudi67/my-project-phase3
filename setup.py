# setup.py
# Packaging setup for the Health Simplified CLI Application

from setuptools import setup, find_packages

setup(
    name='health_simplified',
    version='0.1.0',
    description='Health Simplified CLI Application',
    author='Student',
    packages=find_packages(),
    install_requires=[
        'click',
        'SQLAlchemy',
    ],
    entry_points={
        'console_scripts': [
            'myapp=health_tracker.cli:cli',
        ],
    },
    python_requires='>=3.7',
)
