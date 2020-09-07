#!/usr/bin/env bash

MAX_WAIT=60 # max. 1 minute waiting time in loop before timeout

source ci/faf-rabbitmq.env
docker run --rm -d -p 5672:5672 --env-file ci/faf-rabbitmq.env --name faf-rabbitmq-test rabbitmq:3.8.2-management-alpine

# Create RabbitMQ users
docker exec faf-rabbitmq-test rabbitmqctl wait --timeout ${MAX_WAIT} "${RABBITMQ_PID_FILE}"

docker exec faf-rabbitmq-test rabbitmqctl add_vhost "${RABBITMQ_LEAGUE_SERVICE_VHOST}"
docker exec faf-rabbitmq-test rabbitmqctl add_user "${RABBITMQ_LEAGUE_SERVICE_USER}" "${RABBITMQ_LEAGUE_SERVICE_PASS}"
docker exec faf-rabbitmq-test rabbitmqctl set_permissions -p "${RABBITMQ_LEAGUE_SERVICE_VHOST}" "${RABBITMQ_LEAGUE_SERVICE_USER}" ".*" ".*" ".*"
