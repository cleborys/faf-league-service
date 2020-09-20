# FA Forever - League Service

This is a draft of the [Forged Alliance Forever](http://www.faforever.com/) league service.

## Installation

Install [docker](https://www.docker.com).

The current state depends on a custom version of
[faf-stack](https://github.com/FAForever/faf-stack)
found [here](https://github.com/cleborys/faf-stack/tree/add-faf-league-service).

The following assumes the db container is called `faf-db`,
the database is called `faf-league`,
and the root password is `banana`.
Cloning the above repository and running `scripts/init-db.sh` will set this up.

Additionally, the service needs a running RabbitMQ server, which can be started
via docker by running `ci/init-rabbitmq.sh`,
which starts a RabbitMQ server on vhost `/faf-lobby`.

## Setting up for development

First make sure you have instances of `faf-db` and RabbitMQ running as described in the
installation section. Then install the dependencies to a virtual environment
using pipenv:

    $ pipenv install --dev

If you have just set up the database for development, you will have to apply the
database migrations manually by running

    $ pipenv run migrate-develop

You can now start the service:

    $ pipenv run devserver

**Note** *The pipenv scripts are not meant for production deployment. For
deployment use `faf-stack`*

## Running the tests

Make sure to follow the setup steps above. Then run

    $ pipenv run tests

To run the tests directly in PyCharm you need to add `--mysql_database=faf-league`
in the Additional Arguments field in the Run Configuration.

# License

GPLv3. See the [license](license.txt) file.
