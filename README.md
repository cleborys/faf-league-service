# FA Forever - League Service

This is a draft of the [Forged Alliance Forever](http://www.faforever.com/) league service.

## Installation

Install [docker](https://www.docker.com).

Follow the steps to get [faf-db](https://github.com/FAForever/db) setup, the following assumes the db container is called `faf-db` and the database is called `faf` and the root password is `banana`.
(Most likely that simply means cloning the repository and running `scripts/init_db.sh`.)

Additionally, the service needs a running RabbitMQ server, which can be started
via docker by running `ci/init-rabbitmq.sh`,
which starts a RabbitMQ server on vhost `/faf-lobby`.

Finally, you need to migrate the database manually once to define the new league tables.
To do so run
```
docker cp league_table_migration.sql faf-db:.
docker exec faf-db sh -c "mysql faf -pbanana < league_table_migration.sql"
```

## Setting up for development

First make sure you have instances of `faf-db` and RabbitMQ running as described in the
installation section. Then install the dependencies to a virtual environment
using pipenv:

    $ pipenv install --dev

You can start the service:

    $ pipenv run devserver

**Note** *The pipenv scripts are not meant for production deployment. For
deployment use `faf-stack`*

## Running the tests

Run

    $ pipenv run tests

To run the tests directly in PyCharm you need to add `--mysql_database=faf`
in the Additional Arguments field in the Run Configuration.

## Other tools

You can check for possible unused code with `vulture` by running:

    $ pipenv run vulture

# License

GPLv3. See the [license](license.txt) file.
