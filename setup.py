from setuptools import setup, find_packages

setup(
    name="pycalc",
    version="1.0",
    packages=find_packages(exclude=['tests']),
    author="Dmitry Humeniuk",
    author_email="dhumeniuk@google.com",
    description="Pure-python command-line calculator.",
    license="MIT",
    keywords="calculator",
    url="https://github.com.com/humeniukd/pycalc/",
    project_urls={
        'Bug Reports': 'https://github.com.com/humeniukd/pycalc/issues',
        "Source Code": "https://github.com.com/humeniukd/pycalc/",
    },
    entry_points={  # Optional
        'console_scripts': [
            'pycalc=pycalc:main',
        ],
    },
)
