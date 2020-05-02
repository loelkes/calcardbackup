import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calcardbackup", # Replace with your own username
    version="0.1.0",
    author="Christian Lölkes",
    author_email="christian@loelkes.com",
    description="Backup Nextcloud calendars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loelkes/calcardbackup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'caldav',
        'docopt',
        'icalendar',
        'sqlalchemy'
    ]
)
