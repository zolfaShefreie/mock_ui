import requests
import ast


def get_token():
    url = "http://127.0.0.1:9090/login"

    payload = "{\n    \"username\": \"golestan\",\n    \"password\": \"1\"\n}"
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    dict_res = ast.literal_eval(response.text)
    return dict_res['access']['token']


def save_user_in_auth(payload):
    token = get_token()
    url = "http://127.0.0.1:9090/signup"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return ast.literal_eval(response.text)