# Music Library MVP
This is a python application which interfaces with mongoDB to read and updates a collection in that database.
Ideallistically the Flask app would be deployed using Docker Swarm or Kubernetes (not currently setup).

[![Build Status](https://travis-ci.org/rixka/music-library-mvp.svg?branch=master)](https://travis-ci.org/rixka/music-library-mvp)

#### Dependencies

_Note: This project assumes **virtualenv**, **docker**, and **docker-compose** are installed locally._

Virtual env can be installed with pip:
```
pip install virtualenv
```

To install [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install/) please review the appropriate documentation.


### Requirements Specification:
- JSON API Driven backenend written in Python.
- Data is stored in MongoDB, sample data provided `songs.json`.
- Anticipating massive scale with the Database growing to millions of documents.
- This backend will support a popular application with millions of users including unexpected spikes in activity.


### Quick Start with Docker

```shell
make docker-up # or `make docker-up-mongo` to only setup mongoDB
make docker-logs

# Kill with fire
make docker-down
```

Or if preferred:
```shell
docker-compose build
docker-compose up

# Kill with fire
docker-compose down
```

Once the API and mongoDB containers are running you can curl requests or navigate with the browser `http://localhost:5000/songs`.

#### Example - curl
```
curl -v http://localhost:5000/songs

# example id
curl -v "http://localhost:5000/songs?last-id=5aae8dd659b58a3eb2973b6c"
```


### Quick testing
```shell
make docker-up-mongo
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


## Future Work

* **LOGGING!!!!!!**
* **LOGGING!!!!!!**
* And more **logging** - possibly look into integrating sentry.
* GraphQL.
* Build and push api image to a docker registry for production use.
* Appropriate API documentation (i.e Swagger).
* Meaningful Error messages (i.e Bad Request - invalid parameter).
* Unit tests with mocks bypassing Flask and MongoDB.
* Breakdown the code into more modular components.
* The tests should continue to grow, separating them out may become necessary.
* OAuth 2.0.
* JSON transformation on the outputs, the `_id` is a bit unsightly.

_Note: Feedback welcomed._
