from typing import Annotated
from datetime import date, datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

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

@app.put("/db/aggiungi")
def aggiungi(user: Users, session: SessionDep) -> Users:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/db/trova/{id}")
def trova(id: int, session: SessionDep) -> Users:
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
    richiesta = session.exec(select(Users).where((Users.data >= data) & (Users.data <= oggi))).all()
    if richiesta is None:
        raise HTTPException(status_code=404, detail="User not found")
    return richiesta

@app.get("/db/numero/utenti")
def numero_utenti(session: SessionDep):
    utenti = session.exec(select(Users)).all()
    numero = len(utenti)
    return numero