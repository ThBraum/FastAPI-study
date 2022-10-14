from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Animal(BaseModel):
    id: Optional[str]
    nome: str
    idade: int
    sexo: str
    cor: str

banco: List[Animal] = []

@app.get('/animais')
async def listar_animais():
    return banco

@app.get('/animais/{animal_id}')
def obter_animal(animal_id: str):
    #return {"id": animal_id}
    for animal in banco:
        if animal.id == animal_id:
            return animal
    return {"erro": "animal nao encontrado"}

@app.delete('/animais/{animal_id}')
def remover_animal(animal_id: str):
    posicao = -1
    #buscar a posicao do animal
    for index, animal in enumerate(banco): #enumerate retorna a posicao e o obj
        if animal.id == animal_id:
            posicao = index
            break
    
    if posicao != -1:
        banco.pop(posicao)
        return {"mensagem": "Animal removido com sucesso"}
    else:
        return {"erro": "animal nao encontrado"}

@app.post('/animais')
def criar_animal(animal: Animal):
    animal.id = str(uuid4())
    banco.append(animal)
    return None
