set PATH=%PATH%;C:\Users\marcello.semboli\AppData\Local\Programs\Python\Python36\Scripts\
rem pybabel extract -F babel.cfg -o messages.pot .
rem pybabel init -i messages.pot -d translations -l it
rem pybabel update -i messages.pot -d translations
pybabel compile -d translations
pause

