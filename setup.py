# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

from typing import List

import setuptools

with open('README.md') as i:
    _long_description = i.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

requirements_dev: List[str] = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='scabot',
    version='1.0.0',
    author='Konrad Weihmann',
    author_email='kweihmann@outlook.com',
    description='SCA automation bot',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license_files=('LICENSE',),
    url='https://github.com/priv-kweihmann/scabot',
    packages=setuptools.find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'scabot = scabot.__main__:main',
        ],
    },
    install_requires=requirements,
    extras_require={
        'dev': requirements_dev,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Quality Assurance',
    ],
    python_requires='>=3.6',
)
