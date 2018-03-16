# Music Library MVP
This is a python application which interfaces with mongoDB to read and updates a collection in that database.

[![Build Status](https://api.travis-ci.org/rixka/music-library-mvp.svg?branch=master)](https://api.travis-ci.org/rixka/music-library-mvp.svg)

_Note: This project assumes virtualenv and docker is installed_

### Requirements:
- JSON API Driven backenend written in Python.
- Data is stored in MongoDB, sample data provided `songs.json`.
- Anticipating massive scale with the Database growing to millions of documents.
- This backend will support a popular application with millions of users including unexpected spikes in activity.


### Quick Start with Docker

```shell
make docker-up
make docker-logs
make docker-down
```

Or if preferred:
```shell
docker-compose build
docker-compose up
docker-compose down
```

### Quick testing
```shell
make venv
make test
```

Or if preferred:
```shell
python setup.py test
```

All tests are run using pytest:
```shell
pytest -vvra tests
```

### Quick cleaning with Docker
```shell
docker rm `docker ps -aq`
docker volume rm `docker volume ls -q -f dangling=true`
docker rmi `docker images --filter "dangling=true" -q --no-trunc`
```

_Note: More information available [here](https://gist.github.com/bastman/5b57ddb3c11942094f8d0a97d461b430)._

