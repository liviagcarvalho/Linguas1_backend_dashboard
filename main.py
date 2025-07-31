from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect
#from models.task import Task # Importa o modelo de dados da tarefa

app = FastAPI()

# Conexão com o MongoDB Atlas
#connect(db="todo_app", host="sua_connection_string_aqui")

# CORS (Não se preocupe com isso por enquanto, é uma configuração de segurança que permite que o frontend acesse a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)