@echo off
md \opt\voting\database\
del \opt\voting\database\copernico-spritz.sqlite3.db
sqlite3 \opt\voting\database\copernico-spritz.sqlite3.db < create.sql
pause
