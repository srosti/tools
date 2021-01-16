# simple script to toggle the DNS server 
# background- used to enable/disable youtube for kids by either using opendns(disabled) or sparklight's(enabled) DNS servers

import requests
from  requests.auth import HTTPBasicAuth
import json

password = '###########'

response = requests.get('http://10.10.10.1/api/config/dns/', auth=HTTPBasicAuth('admin', password))

print('current dns')
print(response.json())

dns_info = response.json()['data']

if response.json()['data']['mode'] == 'auto':
    dns_info['mode'] = 'static'
else:
    dns_info['mode'] = 'auto'

print('new dns')
print(dns_info)

response = requests.put('http://10.10.10.1/api/config/dns', data={'data': json.dumps(dns_info)}, auth=HTTPBasicAuth('admin', '!QAZ2wsx'))

print('final response')
print(response.json())
