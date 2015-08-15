from setuptools import setup, find_packages

setup(
    name = 'travis-sphinx',
    version = '0.0.1',
    description=('Manages building sphinx documentation and deploying documentation to gh-pages via travis'),
    author='Grant Mercer',
    author_email='gmercer015@gmail.com',
    url='https://github.com/syntaf/travis-sphinx',
    download_url='https://github.com/syntaf/travis-sphinx/tarball/0.0.0',
    keywords=['documentation', 'travis', 'python', 'deploy'],
    packages = find_packages(),
    py_modules = ['travis_sphinx'],
    entry_points = {
        'console_scripts' : ['travis-sphinx=travis-sphinx:main']
    },
    classifiers = ['Topic :: Software Development :: Documentation',
                   'Programming Language :: Python'],
)

