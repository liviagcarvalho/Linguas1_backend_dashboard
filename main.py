# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd

# app = FastAPI()

# # Permitir conexão com o React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Em produção, especifique o domínio
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/aulas")
# def get_aulas():
#     df = pd.read_csv("Aulas.csv")
#     return df.to_dict(orient="records")

# @app.get("/base")
# def get_base():
#     df = pd.read_csv("base_tratada_lingualab2 - cópia.csv")
#     return df.to_dict(orient="records")


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from Homepage import router as homepage_router  # importe o router

app = FastAPI()

# Permitir conexão com o React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Suas rotas atuais
@app.get("/aulas")
def get_aulas():
    df = pd.read_csv("Aulas.csv")
    return df.to_dict(orient="records")

@app.get("/base")
def get_base():
    df = pd.read_csv("base.csv")
    return df.to_dict(orient="records")



