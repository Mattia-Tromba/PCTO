from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

lista= []
@app.get("/test/{x}")
def read_root(x):
    y= int (x)
    lista.append(y)
    print(lista)
    return lista