from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="shelvr",
    version="0.1.1",
    description="A smart CLI file organizer that cleans clutter",
    long_description=long_description,
    long_description_content_type="text/markdown",  # ✅ Required for Markdown on PyPI
    author="Vaibhav Tiwari",
    packages=find_packages(),
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "shelvr = shelvr.cli:main",
        ]
    },
    python_requires=">=3.6",
)
