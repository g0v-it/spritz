rem After messages.po file is translated, run this to compile a messages.mo file.
rem pybabel extract -F babel.cfg -o messages.pot .
rem pybabel init -i messages.pot -d translations -l it
rem pybabel update -i messages.pot -d translations
pybabel compile -d translations
pause

