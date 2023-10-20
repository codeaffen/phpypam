#!/bin/bash

exec 10>&1
exec > /dev/null 2>&1

function info() {
    echo "${@}" >&10
}

MYSQL_PING="mysqladmin ping -h ${DB_HOST:-127.0.0.1} -P ${DB_PORT:-3306} -u ${MYSQL_ROOT_USER:-root} -p${MYSQL_ROOT_PASSWORD:-rootpw}"

if grep -q podman <<< $(docker --version 2> /dev/null) ; then
  info "Podman is installed"
  DOCKER_CMD=$(which podman)
fi

if "${DOCKER_CMD}" ps | grep -q docker_phpipam_1 && ! eval "${MYSQL_PING}" ; then

    info -n "Waiting for database connection "
    while ! eval "${MYSQL_PING}" ; do
        info -n "."
        sleep 1
    done
    info
fi

info "Database is up"

if [[ $(mysqlshow -u root -prootpw -h 127.0.0.1 -P 3306 phpipam | wc -l) -eq 5 ]] ; then

    info "Creating database ${DB_NAME:-phpipam}"
    ${DOCKER_CMD} exec -ti docker_phpipam_1 sh -c 'mysql -h database -u phpipam -pphpipamadmin phpipam < /phpipam/db/SCHEMA.sql' && ((init_result++))

    info "Activating API"
    mysql -u phpipam -pphpipamadmin -h "${DB_HOST:-127.0.0.1}" phpipam --execute="UPDATE settings SET api=1 WHERE id=1;" && ((init_result++))

    info "Inserting API application"
    mysql -u phpipam -pphpipamadmin -h "${DB_HOST:-127.0.0.1}" phpipam --execute="INSERT INTO api (app_id, app_code, app_permissions, app_security, app_lock_wait) VALUES ('ansible','aAbBcCdDeEfF00112233445566778899',2,'ssl_token',0);" && ((init_result++))

    info "Disable forced password reset"
    mysql -u phpipam -pphpipamadmin -h "${DB_HOST:-127.0.0.1}" phpipam --execute="UPDATE users SET passChange = 'No' WHERE username = 'Admin';" && ((init_result++))

    [ "$init_result" -eq 4 ] && result=successful || result=failed

else

    info "Detabase already initiated" && exit 0

fi

info "Database initialisation $result"
