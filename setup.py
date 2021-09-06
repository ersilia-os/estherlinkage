import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="estherlinkage",
    version="0.0.1",
    author="Miquel Duran-Frigola",
    author_email="miquel@ersilia.io",
    description="ESTHER record linkage course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ersilia-os/estherlinkage",
    project_urls={
        "GitBook": "https://ersilia.gitbook.io/esther-workshop/",
    },
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["utilities"]),
    python_requires=">=3.6",
)
