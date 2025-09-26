import json
from typing import Annotated
from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import secrets, re, string

app = FastAPI()

#connessione al database
urldb = "sqlite:///./test.db"
connessione = {"check_same_thread": False}
engine = create_engine(urldb)

#modello tabella database
class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    token: str = Field(unique=True)
    data: date = Field(default=None)

def crea_tabella():
    SQLModel.metadata.create_all(engine)

#sessione (salvataggio e modifica oggetti nel database)
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/db/create")
def create():
    crea_tabella()
    return {"table": "created"}

@app.put("/db/registrazione")
def registrazione(email: str, session: SessionDep):
    if re.match(r'^\w+@\w+\.\w', email):
        caratteri = string.ascii_letters + string.digits
        tk = ''.join(secrets.choice(caratteri) for _ in range(26))
        user = Users(email=email, token=tk, data=date.today())
        session.add(user)
        session.commit()
        return {"registrazione completata": "token: %s" %tk}
    raise HTTPException(status_code=400, detail="Email non valida")

@app.get("/db/autenticazione")
def autenticazione(email: str, token: str, session: SessionDep):
    user = session.scalars(select(Users).where(Users.email == email)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Email non valida")
    if user.token != token:
        raise HTTPException(status_code=404, detail="Token non valido")
    return {"autenticazione" : "effettuata"}

@app.get("/db/intervallo")
def intervallo(id1, id2: int, session: SessionDep):
    dict = {}
    for x in range(int(id1), int(id2)+1):
        user = session.get(Users, x)
        if user is None:
            raise HTTPException(status_code=404, detail="First user not found")
        dict.update({f"user_{x}": user.email})
    return dict

@app.put("/db/cambiatoken")
def cambiatk(email: str, token: str, session: SessionDep):
    user = session.scalars(select(Users).where(Users.email == email)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if user.token == token:
        caratteri = string.ascii_letters + string.digits
        tk = ''.join(secrets.choice(caratteri) for _ in range(26))
        user.token = tk
        session.commit()
        return {"token": "aggiornato"}
    raise HTTPException(status_code=404, detail="Token non valido")