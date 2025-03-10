from setuptools import setup, find_packages

setup(
    name="sswitch",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "sswitch=sswitch.sswitch:main",
        ],
    },
    author="Your Name",
    description="A simple SSH config updater with customizable config location",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sswitch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)