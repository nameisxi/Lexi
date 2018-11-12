import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lexi",
    version="0.0.1",
    author="Tuomas Peltonen",
    author_email="tuomas.j.j.peltonen@gmail.com",
    description="Sentiment classifier and lexicon creator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nameisxi/Lexi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)