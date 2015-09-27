docker run --name mysql-client -it --link db:mysql --rm mariadb sh -c 'exec mysql -uroot -ptest -hmysql'
