import requests
from requests.auth import HTTPBasicAuth
url = 'http://127.0.0.1:5000'
#logs in and in order
# r = requests.get(url+'/books',data = {'order':'Author','ascending':'true'},auth=HTTPBasicAuth('admin', 'admin'))
r = requests.get(url+'/books/206',auth=HTTPBasicAuth('admin', 'admin'))
print(r.text)
