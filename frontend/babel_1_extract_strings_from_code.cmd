rem this commands extract text from source code
pybabel extract -F babel.cfg -o messages.pot .
rem pybabel init -i messages.pot -d translations -l it
pybabel update -i messages.pot -d translations
rem pybabel compile -d translations
echo Now edit translations/xx/LC_MESSAGES/messages.po files in your language
pause

