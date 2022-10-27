initial file for main branch


docker-compose - 1.29.2
docker - 20.10.12

потрібен файл .env для docker-compose і postgresql у папці back.
аргументи:
- PG_DB - db name
- PD_USER - db user
- PG_PASS - db password 
- PG_HOST - db host
- PG_PORT - db port

to run docker-compose use 'docker-compose build && docker-compose up'
