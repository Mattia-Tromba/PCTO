import requests

#r=requests.post("http://127.0.0.1:8000/db/create")
#a = requests.get("http://127.0.0.1:8000/db/iscrizioni/dal/2025-09-28/ad/oggi")
b = requests.get("http://127.0.0.1:8000/db/numero/utenti")
c= requests.delete("http://127.0.0.1:8000/db/rimuovi/caparezza/iovengodallaluna")
print(c.text)
print(b.text)
"print (r.text)"
"print(a.text)"
