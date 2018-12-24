@echo off
copy create.sql create.sql.old
sqlite3 \opt\voting\database\copernico-spritz.sqlite3.db .dump > create.sql
pause
