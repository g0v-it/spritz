rem @echo off
set PATH=%PATH%;C:\Program Files\MariaDB 10.6\bin
copy create.mysql.sql create.mysql.old
mariadb-dump  -h localhost -u root -p spritz > create.mysql.sql
pause
