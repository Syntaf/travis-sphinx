travis-sphinx [![Build Status](https://travis-ci.org/Syntaf/travis-sphinx.svg?branch=master)](https://travis-ci.org/Syntaf/travis-sphinx)
================
A standalone script for automated building and deploying of sphinx docs via travis-ci

#### What does it do? 

travis-sphinx aims to take the hassle out of building and pushing docs to your gh-pages. deploying to your github page can be tedious especially when you're making many small changes overtime or even just making a minor revision you'd like to see live; `travis-sphinx` will automate your build and deploy process with the help of [travis-ci](https://travis-ci.org/)! 

* [Installation](#installation)
* [Getting Started](#getting-started)
  * [Obtaining a personal access token](#obtaining-a-personal-access-token)
  * [Calling travis-sphinx](#calling-travis-sphinx)
* [Example](#example-configuration)
* [Help](#help)

*Check out [dnppy](https://github.com/NASA-DEVELOP/dnppy) for a live example of `travis-sphinx` in action!*

Installation
==============
```
pip install --user travis-sphinx
export PATH=$HOME/.local/bin:$PATH
```

Getting Started
======
If you aren't already familiar with travis-ci, take a look at their [getting-started guide](http://docs.travis-ci.com/user/getting-started/). Otherwise the steps below will outline how to get travis-sphinx running in your repository

The first step you'll need to do is simply make sure you have a gh-pages branch that exists, if it doesn't:
```
git checkout -b gh-pages
git rm -rf .
git push --set-upstream origin gh-pages
```

#### Obtaining a Personal Access Token

travis-sphinx requires a *personal access token* to be able to push changes to `gh-pages`, so you'll need to generate a token to use. Head over to your github account settings:

![img](http://i.imgur.com/eKN3YFl.png)

To generate a token: go to *personal access tokens* and click *generate new token*. Make sure to copy this to your clipboard for the next step!

![img](http://i.imgur.com/yDZRDhI.png)

The easiest way to set this token is to head over to https://travis-ci.org/ and click on *settings* for the repository you'll be using travis-sphinx with. You can add the token by specifying it in the enviroment variable under the name `GH_TOKEN`. You can also follow [this](http://www.hoverbear.org/2015/03/07/rust-travis-github-pages/#givingtravispermissions) tutorial on giving travis permissions, but the first options is much more simple

![img](http://i.stack.imgur.com/J2U27.png)

Now travis-sphinx can push to your gh-pages, all done! The next step is calling travis-sphinx within your `.travis.yml`

#### Calling travis-sphinx
Once your personal access token is setup, you can begin using travis-sphinx within your configuration file. The two calls that should be used are:
```
script:
    - travis-sphinx build
    
after_success:
    - travis-sphinx deploy
```
*build* will generate the actual documentation files while *deploy* will move those files to gh-pages. If you don't have your documentation in the standard `docs/source` path, you can specify **where** they are with `--source`
```
script:
    - travis-sphinx --source=other/dir/doc build
    
after_success:
    - travis-sphinx deploy
```
### Example Configuration
```
language: python - "2.7"

# before_install will simply setup a conda enviroment for installing python packages, if you
# have project dependencies it's usually recommended to go this route
before_install:
    - wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
    - chmod +x miniconda.sh
    - "./miniconda.sh -b"
    - export PATH=/home/travis/miniconda/bin:$PATH
    - conda update --yes conda
    - sudo rm -rf /dev/shm
    - sudo ln -s /run/shm /dev/shm

install:
    - conda install --yes python="2.7" sphinx
    - pip install --user travis-sphinx

script:
    - travis-sphinx build

after_success:
    - travis-sphinx deploy
```

Also see a working example at the [dnppy](https://github.com/NASA-DEVELOP/dnppy) repository

### Help
```
travis-sphinx v0.0.1
Usage: travis-sphinx [options] {actions}

Options:
  -h, --help		Provide information on script or following action
  -s, --source		Source directory of sphinx docs, default is docs/source
  -n, --nowarn      Do no error on warnings
Actions:
  build 		Build sphinx documentation
  deploy		Deploy sphinx docs to travis branch
```

