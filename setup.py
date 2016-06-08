import os
import codecs

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name='pymixup',
    version=__import__('common').__version__,
    packages=find_packages(),
    include_package_data=True,
    keywords="python obfuscate pymixup",
    description='An app to obfuscate Python projects',
    long_description=codecs.open(
        os.path.join(os.path.dirname(__file__), 'README.rst'),
        encoding='utf-8').read(),
    install_requires=[
        'Fabric>=1.11.1',
        'peewee>=2.8.1',
        'pyparsing>=2.1.1',
    ],
    url='http://github.com/rdevost/pymixup',
    author='Richard DeVost',
    author_email='richard@devost.org',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ]
)
