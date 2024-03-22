import requests
import json

params = {"apiLogin" : "69e23f61"}

response = requests.post('https://api-ru.iiko.services/api/1/access_token', json=params)
j_resp = response.json()

iiko_token = j_resp.get('token')

headers = {
    "Authorization": f'Bearer {iiko_token}',
}

def guest_categories(phone):

    params2 = {
        "phone": phone,
        "type": "phone",
        "organizationId": "64f45e6f-f38a-4d58-8c62-cc7fa3cb499a"
    }

    guest_resp = requests.post('https://api-ru.iiko.services/api/1/loyalty/iiko/customer/info', headers=headers, json=params2)
    ja = guest_resp.json()

    js = []
    for key in ja['categories']:
        js.append(key["name"])

    return js

def guest_balance(phone):

    params2 = {
        "phone": phone,
        "type": "phone",
        "organizationId": "64f45e6f-f38a-4d58-8c62-cc7fa3cb499a"
    }

    guest_resp = requests.post('https://api-ru.iiko.services/api/1/loyalty/iiko/customer/info', headers=headers, json=params2)
    ja = guest_resp.json()
    print(ja)

    jj = []
    for key in ja['walletBalances']:
        jj.append(f'{key["name"]} : {key["balance"]}')

    return jj
