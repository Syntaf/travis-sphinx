from setuptools import setup, find_packages

setup(
    name = 'travis-sphinx',
    version = '2.2.0',
    description='Manages building sphinx documentation and deploying documentation to gh-pages via travis',
    author='Grant Mercer',
    author_email='gmercer015@gmail.com',
    url='https://github.com/syntaf/travis-sphinx',
    download_url='https://github.com/Syntaf/travis-sphinx/archive/master.zip',
    keywords=['documentation', 'travis', 'python', 'deploy'],
    packages = find_packages(),
    py_modules = ['travis_sphinx'],
    entry_points = {
        'console_scripts' : ['travis-sphinx=travis_sphinx.main:main']
    },
    install_requires=[
        'sphinx',
        'click',
        'ghp-import',
    ],
    classifiers = [
        'Topic :: Software Development :: Documentation',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)