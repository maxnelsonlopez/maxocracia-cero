from setuptools import find_packages, setup

setup(
    name="maxocracia",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "flask-limiter>=2.0.0",
        "pyjwt>=2.0.0",
        "werkzeug>=2.0.0",
        "pytest>=6.0.0",
        "pytest-cov>=2.0.0",
    ],
    python_requires=">=3.8",
)
