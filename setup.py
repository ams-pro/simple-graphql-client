import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-graphql-client",
    version="0.0.4",
    author="Fabian Riewe",
    author_email="f.riewe@ams-pro.de",
    description="A simple graphql client which also supports file upload",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ams-pro/simple-graphql-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests==2.22.0",
        "graphql-server-core==1.2.0"
    ]
)
