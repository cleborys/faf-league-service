#!/bin/bash
set -e


echo 'travis_fold:start:bootstrap_database'
echo '# Build & Run Database Docker Container'
docker network create faf
docker run --network="faf" --network-alias="faf-db" -p 3306:3306\
           -e MYSQL_ROOT_PASSWORD=banana \
           -e MYSQL_DATABASE=faf-league \
           --rm -d --name faf-db \
           mysql:5.7

echo -n 'Waiting on faf-db container'
counter=1
# wait 5 minutes on docker container
while [ $counter -le 300 ]
do
    if docker exec -it faf-db sh -c "mysqladmin ping -h 127.0.0.1 -uroot -pbanana" &> /dev/null; then

        docker exec -i faf-db mysql --user=root --password=banana <<SQL_SCRIPT
          CREATE DATABASE IF NOT EXISTS \`faf-league\`;
          CREATE USER 'faf-league-service'@'%' IDENTIFIED BY 'banana';
          GRANT ALL PRIVILEGES ON \`faf-league\`.* TO 'faf-league-service'@'%';
SQL_SCRIPT

        echo 'travis_fold:end:bootstrap_database'

        exit 0
    fi
    echo -n "."
    sleep 1
    ((counter++))
done
echo 'Error: faf-db is not running after 5 minute timeout'
echo 'travis_fold:end:bootstrap_database'
exit 1
