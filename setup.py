from setuptools import setup, find_packages

setup(
    name="language_mentor",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "gradio",
        "pytest",
    ],
) 