import requests

r = requests.get("http://127.0.0.1:8000/db/trova/9")
print(r.text)
#oj