import requests
from guest_request import iiko_token

headers = {
    "Authorization": f'Bearer {iiko_token}',
}

def guest_id(phone):

    params2 = {
        "phone": phone,
        "type": "phone",
        "organizationId": "64f45e6f-f38a-4d58-8c62-cc7fa3cb499a"
    }

    guest_resp = requests.post('https://api-ru.iiko.services/api/1/loyalty/iiko/customer/info', headers=headers, json=params2)
    global ja
    ja = guest_resp.json()
    return ja["id"]


def guest_refill(sum):
 
    params3 = {
        "customerId": ja["id"],
        "walletId": "ccfb9e91-4eb4-11e8-80cd-d8d385655247", #const
        "sum": sum,
        "comment": "Начислено через бота",
        "organizationId": "64f45e6f-f38a-4d58-8c62-cc7fa3cb499a"  #const  
    }

    requests.post('https://api-ru.iiko.services/api/1/loyalty/iiko/customer/wallet/topup', headers=headers, json=params3)
    # https://api-ru.iiko.services/api/1/loyalty/iiko/customer/wallet/chargeoff списание баланса

guest_id('79130163304')