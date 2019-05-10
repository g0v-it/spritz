set PATH=%PATH%;C:\Users\marcello.semboli\AppData\Local\Programs\Python\Python36\Scripts\
pybabel extract -F babel.cfg -o messages.pot .
rem pybabel init -i messages.pot -d translations -l it
pybabel update -i messages.pot -d translations
rem pybabel compile -d translations
pause

