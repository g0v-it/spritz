rem @echo off
set PATH=%PATH%;C:\Program Files\PostgreSQL\11\bin
dropdb -h localhost -U dinogen spritz
createdb -h localhost -U dinogen spritz
psql -h localhost -U dinogen spritz < create.sql
psql -h localhost -U dinogen spritz < alter.001.sql
pause