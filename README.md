[![Build Status](https://travis-ci.org/team-n3m/n3m.png?branch=master)](https://travis-ci.org/team-n3m/n3m)
[![Coverage Status](https://coveralls.io/repos/github/team-n3m/n3m/badge.svg?branch=master)](https://coveralls.io/github/team-n3m/n3m?branch=master)
[![Downloads][downloads-image]][downloads-url]
[![NPM version][npm-image]][npm-url]

# n3m
The repo for the n3m team app. It is awesome!

To get started some prerequisites should be installed. To begin make sure you have python and that it's using version 2.7.

### Local Install
1. Pip (https://pip.pypa.io/en/latest/installing.html)
  1. wget https://bootstrap.pypa.io/get-pip.py
  2. python get-pip.py
2. PostgreSQL (http://www.postgresql.org/download/)
3. NPM (https://docs.npmjs.com/getting-started/installing-node)


### Alternatively Use Docker
You can use the docker file included in this repo which will create a working development environment for you. To do so perform these steps. The initial docker build will take a while:

1. Install Docker (https://www.docker.com/products/docker)
2. execute the following commands from the repository root:
```
sh build_docker.sh 
sh run_docker.sh

```
3. This will bring you to a command prompt with everything installed, the database daemon started, the app ready to start running. 

docker start -ai n3m

After that run 
```
sh server.sh &
sh web.sh &
```
You should then be able to access the web interface of the app from your local dev machine at http://localhost:5000. Note that you cannot have a running process on your host machine at port 5000..

Make sure you allow your browser to access your geo location for Uber and OpenTable APIs.

### Checkout out the docs for more information:
[Documentation](docs/Documentation.md)

[npm-image]: https://img.shields.io/npm/v/eslint.svg?style=flat-square
[npm-url]: https://www.npmjs.com/package/eslint
[downloads-image]: https://img.shields.io/github/downloads/team-n3m/n3m/latest/n3m.svg
[downloads-url]: https://github.com/team-n3m/n3m
