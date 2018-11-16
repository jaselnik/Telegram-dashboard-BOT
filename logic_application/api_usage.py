import requests
import json
import time

URIS = {
    'add_start': '/addAccount/start',
    'add_query': '/addAccount/query',
    'verify_start': '/verify/start',
    'verify_query': '/verify/query',
}
ERROR_RESPONSES = {
    'Task still running': True,
    'No task running': False,
    'time out': False,
    'NA': False
}
IP = '136.243.15.225'
PORT = '8888'
URL = 'http://{0}:{1}/RCS{2}'


def _request(url, data=None, method='GET'):
    if method == 'GET':
        print('======GET======')
        res = requests.get(url, data)
        print(res.text)
        return json.loads(requests.get(url, data).text)
    if method == 'POST':
        print('======POST======')
        res = requests.post(url, data)
        print(res.text)
        return


def add_account(data):
    _ = _request(URL.format(IP, PORT, URIS['add_start']), data, 'POST')
    print('===GOT===')
    while True:
        response = _request(URL.format(IP, PORT, URIS['add_query']))
        print('===GOT2===')
        if response.get('success'):
            return 'please entry the code'
        elif response.get('error'):
            if ERROR_RESPONSES[response.get('error')]:
                time.sleep(2)
            else:
                return 'Something goes wrong. Please, check your credentials'
        else:
            raise Exception('InvalidResponse. Error with /addAccount/')


def verify(data):
    _ = _request(URL.format(IP, PORT, URIS['verify_start']), data, 'POST')
    while True:
        response = _request(URL.format(IP, PORT, URIS['verify_query']))
        if response.get('success'):
            return 'Successfully added'
        elif response.get('error'):
            if ERROR_RESPONSES[response.get('error')]:
                time.sleep(2)
            else:
                return 'Something goes wrong. Please, check your credentials'
        else:
            raise Exception('InvalidResponse. Error with /verify/')
