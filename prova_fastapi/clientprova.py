import requests

r = requests.put("http://127.0.0.1:8000/db/registrazione", params={"email": "mattiatromba07@gmail.com"})
print(r.text)

r = requests.get("http://127.0.0.1:8000/db/autenticazione", params={"email": "f@gmail.com", "token": "dYxRgjQDK4SygRvSRbdzxOygnW"})
print(r.text)

r = requests.get("http://127.0.0.1:8000/db/intervallo", params={"id1": 2, "id2": 5})
print(r.text)

r = requests.get("http://127.0.0.1:8000/db/cambiatoken", params={"id1": 2, "id2": 5})
