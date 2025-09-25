from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

urldb = "sqlite:///./test.db"
connessione = {"check_same_thread": False}
engine = create_engine(urldb)

#modello tabella database
class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)

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

@app.delete("/db/rimuovi/{id}")
def rimuovi(id: int, session: SessionDep):
    user = session.get(Users, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return "user deleted"