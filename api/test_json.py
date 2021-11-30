
if __name__ == '__main__':
    import json
    import requests
    import random

    # TEST LOGIN
    url = 'http://localhost:5000/api/login'
    myobj = {'username': 'aldo', 'password':'aldo'}
    response = requests.post(url, json=myobj)
    print(response.status_code)
    print(response.json())

    # # TEST INSERIMENTO
    # url = 'http://localhost:5000/api/votation'
    # n = random.randint(0,1000000)
    # myobj = {"promoter_user_id": 1,   
    # "votation_description":"prova " + str(n),
    # "description_url":"url 1",
    # "begin_date": "2021-07-18 12:30",
    # "end_date": "2021-07-19 11:30",
    # "votation_type": "maj_jud",
    # "votation_status": 0,
    # "list_voters": 0,
    # "options_text": "A\nB\nC",
    # "judgement_text":"X\nY\nZ"
    # }
    # response = requests.post(url, json=myobj)
    # print(response.status_code)
    # print(response.json())

    # # TUTTE LE VOTAZIONI
    # url = 'http://localhost:5000/api/votation'
    # response = requests.get(url)
    # print(response.status_code)
    # print(response.json())

    # UNA VOTAZIONE PER ID
    url = 'http://localhost:5000/api/votation/1'
    response = requests.get(url)
    print(response.status_code)
    print(response.json())

