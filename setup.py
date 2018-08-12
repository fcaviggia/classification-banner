from distutils import log
import os
import sys
from setuptools import setup, find_packages

VERSION = "1.7.0"

PACKAGE_VERSION = {
    "classification-banner": "classification-banner == {}".format(VERSION),
}


setup(
    name="classification-banner",
    version=VERSION,
    description="Displays Classification Banner for a Graphical Session",
    long_description="""Classification Banner is a python script that will display the
classification level banner of a session with a variety of
configuration options on the primary screen.  This script can
help government and possibly private customers display a 
notification that sensitive material is being displayed - for 
example PII or SECRET Material being processed in a graphical
session. The script has been tested on a variety of graphical
environments such as GNOME2, GNOME3, KDE, twm, icewm, and Cinnamon.""",
    license="GPLv2",
    author="Frank Caviggia",
    author_email="fcaviggia@gmail.com",
    maintainer="classification-banner Developers",
    url="https://github.com/fcaviggia/classification-banner",
    download_url="https://github.com/fcaviggia/classification-banner",
    platforms=["Linux"],
    python_requires=">=2.7.5,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        ("License :: OSI Approved :: "
         "GNU General Public License v3 (GPLv3)"),
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Topic :: Security",
    ],
    packages=find_packages(),
    scripts=["bin/classification-banner"],
    data_files=[('share/banner.conf', ['share/classification-banner-screenshot.png']),
                ],
)
