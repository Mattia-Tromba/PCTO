import json
from typing import Annotated
from datetime import date, datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import secrets, re, string

app = FastAPI()

urldb = "sqlite:///./test.db"
engine = create_engine(urldb)

#modello tabella database
class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    token: str = Field(unique=True)
    data: date = Field(default=None)

def crea_tabella():
    SQLModel.metadata.create_all(engine)

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
        utenti = session.exec(select(Users)).all()
        for u in utenti:
            if email == u.email:
                raise HTTPException(status_code=400, detail="Email già registrata")
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
        raise HTTPException(status_code=400, detail="Email non valida")
    if user.token != token:
        raise HTTPException(status_code=400, detail="Token non valido")
    return {"autenticazione" : "effettuata"}

@app.get("/db/intervallo")
def intervallo(id1, id2: int, session: SessionDep):
    diz = {}
    for x in range(int(id1), int(id2)+1):
        user = session.get(Users, x)
        if user is not None:
            diz.update({f"user {x}": user.email})
        else:
            continue
    return diz

@app.put("/db/cambiatoken")
def cambiatk(email: str, token: str, session: SessionDep):
    user = session.scalars(select(Users).where(Users.email == email)).first()
    if user is None:
        raise HTTPException(status_code=400, detail="user not found")
    if user.token == token:
        caratteri = string.ascii_letters + string.digits
        tk = ''.join(secrets.choice(caratteri) for _ in range(26))
        user.token = tk
        session.commit()
        return {"token aggiornato": tk}
    raise HTTPException(status_code=400, detail="Token non valido")

@app.get("/db/trova/{id}")
def trova(id: int, session: SessionDep):
    user = session.get(Users, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/db/rimuovi/{email}/{token}")
def rimuovi(email: str, token : str, session: SessionDep):
    persona = session.exec(select(Users).where(Users.email == email, Users.token == token)).first()
    if persona is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(persona)
    session.commit()
    return "user deleted"

@app.get("/db/iscrizioni/dal/{data}/ad/oggi")
def iscrizioni_da(data : date, session: SessionDep):
    oggi = date.today()
    dict = {}
    richiesta = session.exec(select(Users).where((Users.data >= data) & (Users.data <= oggi))).all()
    if richiesta is None:
        raise HTTPException(status_code=404, detail="User not found")
    y = 1
    for x in richiesta:
        dict.update({f"user {y}": x.email})
        y+=1
    return dict

@app.get("/db/numero/utenti")
def numero_utenti(session: SessionDep):
    utenti = session.exec(select(Users)).all()
    numero = len(utenti)
    return numero
