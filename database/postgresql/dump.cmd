rem @echo off
set PATH=%PATH%;C:\Program Files\PostgreSQL\11\bin
copy create.sql create.sql.old
pg_dump  -h localhost -U dinogen spritz > create.sql
pause
