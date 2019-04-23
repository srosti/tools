import urllib.request
import json

ip_addr = '216.64.128.45'
api_key = '78dc1382931b359b037e0eb2e4337167'
result = urllib.request.urlopen("http://api.ipstack.com/{}?access_key={}".format(ip_addr, api_key)).read()
result = result.decode('utf8')

data = json.loads(result)

if 'success' not in data:
    print('{}'.format(data))
else:
    print('Error retrieving Country Code for IP address: {}'.format(ip_addr))