from setuptools import setup, find_packages

setup(
    name="file-organizer",
    version="1.0.0",
    description="A command-line tool to organize files by type",
    author="Your Name",
    packages=find_packages(),
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "file-organizer = file_organizer.cli:main",
        ]
    },
    python_requires=">=3.6",
)
