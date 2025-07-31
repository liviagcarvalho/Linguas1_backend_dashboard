# Handout Desenvolvimento Web - Capacitação 2025.2

## 1. Introdução

Depois das aulas de introdução ao desenvolvimento web, você já tem uma boa ideia de como um sistema web funciona: frontend, backend e banco de dados trabalhando juntos.

Neste handout, você vai **criar uma aplicação de tarefas (To-do list)** utilizando **FastAPI** no backend, **MongoDB** como banco de dados e uma interface simples com **React + Vite**.

> **Atenção:** A prova de desenvolvimento web irá cobrar até os conceitos **básicos** ensinados. Mas durante os **cases**, você será incentivado a aplicar os **conceitos avançados** de arquitetura e organização de código.

> **Atenção:** Em caso de dúvidas, fique a vontade para chamar qualquer coordenador da frente de engenharia.

---

## 2. Configuração inicial

### 2.1 Criando uma conta no MongoDB Atlas e conectando ao MongoDB Compass
1. Acesse o site do [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Crie uma conta gratuita.
3. Após o login, você será direcionado para o painel do Atlas. Crie um novo projeto clicando em "New Project" e dando um nome para o seu projeto.
4. Crie um cluster: Selecione a opção "Free", de um nome para seu cluster, ecolha aws como provedor e selecione uma região próxima a você(sa-east-1).
5. Após a criação do cluster, clique em "Network Access" no menu lateral e adicione o IP 0.0.0.0/0 para permitir conexões de qualquer IP. Em um projeto real, você deve restringir o acesso ao seu IP ou a uma lista de IPs confiáveis(como o do cliente ou o do deploy).
6. Clique em "Clusters" no menu lateral e depois em "Connect". Crie o usuário pedido e anote o nome de usuário e senha.
7. Selecione a opção "Compass" para baixar o MongoDB Compass, que é uma interface gráfica para interagir com o MongoDB. Instale o Compass e conecte-se ao seu cluster usando a string de conexão fornecida pelo Atlas(não se esqueça de substituir <db_password> pela senha do usuário criado). Vale a pena ressaltar que esse primeiro usuário criado é o usuário administrador do banco de dados e diferentes usuários podem ter diferentes permissões de acesso.

### 2.2 Baixando o Postman
Para testar a API, você pode usar o [Postman](https://www.postman.com/downloads/) para enviar requisições HTTP e visualizar as respostas.

### 2.3 Crie um diretório para o projeto
Crie uma pasta para o projeto

### 2.3 Criando um ambiente virtual: venv(Virtual Environment)

Cada novo projeto de Python pode ter dependencias diferentes, um exemplo é uma análise de dados que normalmente usa a biblioteca `pandas` enquanto o jogo desenvolvido na matéria DesSoft(ou DevLife) usa a biblioteca `pygame`. Assim, nós poderíamos instalar todas as bibliotecas de uma vez para nunca precisarmos nos precopar com isso, certo? 

Não. Linguagens de programação e bibliotecas sao atualizadas constantemente, e uma biblioteca pode ser atualizada de forma que não seja mais compatível com o código que você escreveu. Por isso, é importante criar um ambiente virtual(venv) para cada projeto. Uma venv cria uma "nova intalação" do Python exclusiva para aquele projeto, na qual você pode instalar as bibliotecas que quiser apenas nesse ambiente. Ou seja, quando você muda de projeto, basta mudar de ambiente virtual para ter acesso às bibliotecas que você instalou para aquele projeto.

![Imagem venv](static/venv.png)

Para criar um ambiente virtual, siga os passos abaixo:
1. Abra o terminal ou prompt de comando.
2. Navegue até o diretório do seu projeto (Você pode abrir a pasta pelo vscode e abrir o terminal do aplicativo também).
3. Crie o ambiente virtual:
    - No Windows, execute:
        ```bash
        python -m venv venv
        ```
    - Para Linux ou MacOS, execute:
        ```bash
        python3 -m venv venv
        ```
4. Ative o ambiente virtual(Faça isso sempre que abrir um novo terminal para executar o projeto):
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux ou MacOS:
     ```bash
     source venv/bin/activate
     ```

Agora você está dentro do ambiente virtual e pode instalar as dependências necessárias para o seu projeto. Além disso, tente decorar esses comandos, pois você vai precisar deles em todos os projetos que fizer com Python.

### 2.4 Instalando as dependências
Para essa apliçação, você vai precisar instalar o FastAPI e o MongoEngine:
```bash
pip install "fastapi[standard]"
```
```bash
pip install mongoengine
```

## 3. Criando a aplicação

Agora que você já configurou o ambiente, vamos criar a aplicação de tarefas.

### 3.1 Estrutura do projeto
Crie a seguinte estrutura de pastas e arquivos no seu projeto:

```
todo_app(ou o nome que você deu ao projeto)/
├── main.py (Arquivo principal da aplicação, onde vão estar as rotas e a inicialização do FastAPI)
├── models/
│   └── task.py (Modelo de dados da tarefa, onde você define a estrutura do documento no MongoDB, ou seja, quais serão os campos que uma tarefa terá)
```

### 3.2 Definindo o que é uma tarefa
Uma tarefa é um item que o usuário pode adicionar à sua lista de tarefas. Uma tarefa poderia ter campos como: título, descrição, status (pendente ou concluída) e data de criação. 
Entretanto, nesse caso vamos simplificar e considerar apenas o título e o status da tarefa.

No arquivo `models/task.py`, defina o modelo de dados da tarefa:

```python
from mongoengine import * # Importa o MongoEngine para trabalhar com o MongoDB

class Task(Document): # Define a classe Task que herda de Document do MongoEngine que é a classe base para todos os documentos no MongoDB
    title = StringField(required=True) # Aqui definimos que a tarefa terá um campo `title` do tipo StringField, que é obrigatório (required=True)
    done = BooleanField(default=False) # Aqui definimos que a tarefa terá um campo `done` do tipo BooleanField, que indica se a tarefa está concluída ou não, e o valor padrão é False
```
Para entender mais sobre os tipos de campos e classes disponíveis no MongoEngine , você pode consultar a [documentação oficial](https://docs.mongoengine.org) (**Tome cuidado ao consultar IAs para esse tipo de informação, pois elas podem não estar atualizadas**).

### 3.3 Criando o arquivo principal da aplicação
No arquivo `main.py`, você vai configurar o FastAPI e as rotas da sua aplicação. 

Primeiro, importe as bibliotecas necessárias, configure a conexão com o MongoDB e configure o FastAPI:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect
from models.task import Task # Importa o modelo de dados da tarefa

app = FastAPI()

# Conexão com o MongoDB Atlas
connect(db="todo_app", host="sua_connection_string_aqui")

# CORS (Não se preocupe com isso por enquanto, é uma configuração de segurança que permite que o frontend acesse a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Lembra daquela string de conexão que você copiou do MongoDB Atlas e usou no Compass? Cole ela no lugar de `sua_connection_string_aqui`, mas não se esqueça de substituir `<db_password>` pela senha do usuário que você criou.

### 3.4 Criando a primeira rota: Criando uma tarefa
Agora, vamos criar a rota para criar uma nova tarefa. Adicione o seguinte código ao seu arquivo `main.py`:

```python
@app.post("/tasks") # Esse é o decorador que define o endpoint da rota, que será acessado via POST
def create_task(task: dict): # Aqui definimos a função que será executada quando a rota for acessada. O parâmetro `task` é um dicionário que representa a tarefa a ser criada.
    new_task = Task(**task).save() # Cria uma nova instância da classe Task, passando os dados da tarefa como argumentos. O método `save()` salva a tarefa no banco de dados.
    task_dict = new_task.to_mongo().to_dict()
    task_dict["_id"] = str(task_dict["_id"]) # Converte o ID do MongoDB para uma string, pois o MongoDB usa ObjectId que não é serializável diretamente em JSON
    return task_dict # Retorna a tarefa criada como um dicionário
```

Note que não definimos um método .save() para o modelo Task, mas ele funciona porque é herdado da classe Document do MongoEngine, que já possui esse método implementado.

### 3.5 Criando a rota para listar as tarefas
Agora, vamos criar a rota para listar todas as tarefas. Adicione o seguinte código ao seu arquivo `main.py`:

```python
@app.get("/tasks") # Esse é o decorador que define o endpoint da rota, que será acessado via GET
def get_tasks():
    tasks = Task.objects() # Busca todas as tarefas no banco de dados
    result = []
    for task in tasks:
        task_dict = task.to_mongo().to_dict()
        task_dict["_id"] = str(task_dict["_id"])
        result.append(task_dict)
    return result # Retorna uma lista de dicionários representando as tarefas
```

### Testando as rotas
Agora que você já criou as rotas para criar e listar tarefas, é hora de testá-las usando o Postman.
1. Rode a aplicação FastAPI:
   ```bash
   fastapi run main.py
   ```
2. Abra o Postman e crie uma nova requisição.
3. Para criar uma tarefa, selecione o método POST e insira a URL `http://localhost:8000/tasks`. No corpo da requisição(aba Body logo abaixo da URL), selecione "raw", o formato JSON e adicione um objeto JSON representando a tarefa, por exemplo:
   ```json
   {
       "title": "Estudar FastAPI"
   }
   ```
4. Clique em "Send" para enviar a requisição. Você deve receber uma resposta com os dados da tarefa criada.
5. Para listar as tarefas, crie uma nova requisição, selecione o método GET e insira a URL `http://localhost:8000/tasks`. Clique em "Send" e você deve receber uma lista de tarefas.

Um outro jeito (até mais fácil) de testar as rotas é acessar a documentação interativa do FastAPI(Swagger). Basta abrir o navegador e acessar `http://localhost:8000/docs`. Lá você verá as rotas que você criou e poderá testá-las diretamente pela interface. Entretanto, em alguns casos você pode precisar de um token de autenticação para acessar as rotas, o que não é possível fazer pelo Swagger e nesse caso você deve usar o Postman ou outra ferramenta de testes de API.

### 3.6 Outras rotas
Em um sistema de gerenciamento de informações, é comum existirem quatro operações básicas: criar, ler, atualizar e deletar. Essas operações são conhecidas como CRUD (Create, Read, Update, Delete).

Para completar a sua aplicação de tarefas, você deve adicionar as seguintes rotas(Dica: Pesquise na internet):
- **Atualizar uma tarefa**: Crie uma rota que permita atualizar o título e o status de uma tarefa existente. Use o método PUT e a URL `/tasks/{task_id}`, onde `{task_id}` é o ID da tarefa a ser atualizada.
- **Listar uma tarefa específica**: Crie uma rota que permita listar uma tarefa existente selecionada pelo id. Use o método GET e a URL `/tasks/{task_id}`, onde `{task_id}` é o ID da tarefa a ser listada.
- **Deletar uma tarefa**: Crie uma rota que permita deletar uma tarefa existente. Use o método DELETE e a URL `/tasks/{task_id}`, onde `{task_id}` é o ID da tarefa a ser deletada.

Utilize a documentação do mongoengine para procurar os métodos de delete e update e não se esqueça de testar as novas rotas no Postman ou na documentação interativa do FastAPI.

## 4. Frontend com React + Vite
Durante o trainee você já aprendeu a usar o React, por isso vamos apenas criar um frontend simples com o intuito de demonstrar como integrar o frontend com o backend que você criou.

Um ponto importante é que nos projetos da Insper Jr. usamos o typescript, que é uma linguagem baseada em JavaScript que adiciona tipagem estática ao código. Isso ajuda a evitar erros comuns e torna o código mais fácil de entender e manter. Você pode aprender mais sobre TypeScript na [documentação oficial](https://www.typescriptlang.org/docs/).

### 4.1 Criando o projeto com Vite
Para criar um novo projeto React com Vite, siga os passos abaixo:
1. Certifique-se de ter o Node.js instalado na sua máquina. Você pode baixar a versão mais recente do Node.js em [nodejs.org](https://nodejs.org/).
2. Abra o terminal e navegue até o diretório onde você deseja criar o projeto.
3. Execute o seguinte comando para criar um novo projeto React com Vite:
   ```bash
   npm create vite@latest todo-frontend --template react-ts
   ```
   Isso criará uma nova pasta chamada `todo-frontend` com a estrutura básica de um projeto React usando TypeScript.
4. Navegue até a pasta do projeto:
   ```bash
    cd todo-frontend
    ```
5. Instale as dependências do projeto:
   ```bash
   npm install
   ``` 
6. Inicie o servidor de desenvolvimento:
   ```bash
    npm run dev
    ```
Agora você deve ver o projeto rodando no seu navegador em `http://localhost:5173`.

### 4.2 Integrando com o backend
Substitua o conteúdo do arquivo `src/App.tsx` pelo seguinte código:

```tsx
import { useEffect, useState } from "react";

type Task = {
  _id: string;
  title: string;
  done: boolean;
};

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTitle, setNewTitle] = useState("");

  const API_URL = "http://localhost:8000";

  const fetchTasks = async () => {
    const res = await fetch(`${API_URL}/tasks`);
    const data = await res.json();
    setTasks(data);
  };

  const addTask = async () => {
    if (!newTitle.trim()) return;
    await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle }),
    });
    setNewTitle("");
    fetchTasks();
  };

  const toggleTask = async (id: string, current: boolean) => {
    await fetch(`${API_URL}/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ done: !current }),
    });
    fetchTasks();
  };

  const deleteTask = async (id: string) => {
    await fetch(`${API_URL}/tasks/${id}`, {
      method: "DELETE",
    });
    fetchTasks();
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ maxWidth: 500, margin: "2rem auto", textAlign: "center" }}>
      <h1>📝 Lista de Tarefas</h1>

      <input
        type="text"
        value={newTitle}
        onChange={(e) => setNewTitle(e.target.value)}
        placeholder="Nova tarefa"
      />
      <button onClick={addTask}>Adicionar</button>

      <ul style={{ listStyle: "none", padding: 0, marginTop: 20 }}>
        {tasks.map((task) => (
          <li key={task._id} style={{ marginBottom: 10 }}>
            <span
              style={{
                textDecoration: task.done ? "line-through" : "none",
                marginRight: 10,
              }}
            >
              {task.title}
            </span>
            <button onClick={() => toggleTask(task._id, task.done)}>
              {task.done ? "Desmarcar" : "Concluir"}
            </button>
            <button onClick={() => deleteTask(task._id)}>🗑️</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

Para interagir com o backend, usamos a função `fetch` do JavaScript para fazer requisições HTTP. As funções `fetchTasks`, `addTask`, `toggleTask` e `deleteTask` são responsáveis por buscar, adicionar, atualizar e deletar tarefas, respectivamente. A função `fetch` faz exatamente o que o Postman faz, mas de forma programática, ou seja, dentro do código. 

Além isso, perceba que usamos async e await:
- `async` é usado para declarar uma função assíncrona, ou seja, ela não vai bloquear o resto do código enquanto espera.
- `await` é usado dentro das funções para esperar o resultado de uma operação demorada (como fetch ou acesso ao banco de dados).

## 5. Conclusão dos conceitos básicos
Parabéns! Você criou uma aplicação de tarefas completa com FastAPI no backend e React + Vite no frontend. Agora sabe como criar rotas, interagir com o MongoDB e construir uma interface simples para o usuário.

O intuito deste handout é te ajudar a entender os conceitos básicos de desenvolvimento web e como as tecnologias se integram. Agora, uma sugestão é que você tente treinar mais esses conceitos criando novas rotas ou outras aplicações simples.

> **Atenção:** A prova de desenvolvimento web irá cobrar os conceitos ensinados até aqui. Durante a prova, você poderá usar este handout como referência, suas anotações e até mesmo pesquisar na internet. Entretanto, não será permitido o uso de IAs para responder as questões. Por isso, é importante que você entenda os conceitos e saiba aplicá-los.

## 6. Conceitos avançados
Em seguida, serão apresentados alguns conceitos mais avançados sobre desenvolvimento web. Apesar de não serem cobrados na prova, você precisará deles para os cases. 

O intuito a partir daqui não é te ensinar passo a passo como fazer, mas sim te apresentar os conceitos e te dar um direcionamento para que você possa pesquisar e aprender mais sobre eles. Tente realmente entender os conceitos, já que eles serão constantemente utilizados nos projetos reais da Insper Jr. e em projetos futuros que você venha a fazer na graduação ou carreira.

Para guiar você, vamos usar como exemplo a estrutura de um projeto da Insper Jr.

### 6.1 Estrutura de um backend de um projeto da Insper Jr.
Agora que você já sabe como criar uma aplicação com FastAPI, imagine que você precisa criar um projeto de um backend de uma plataforma de educação, como o Blackboard por exemplo. Esse projeto terá vários tipos de entidades, como usuários, cursos, matérias, materiais e etc. Além disso, cada entidade terá suas próprias rotas, funções, modelos de dados e etc. Agora imagine colocar tudo isso em um único arquivo `main.py` como estamos fazendo até aqui. Isso seria uma bagunça, certo?


Por isso, dentro (e fora também) da empresa, são utilizadas diferentes estruturas de projetos que facilitam a organização do código e a manutenção de projetos. Dentro da InsperJr. nossa estrutura é baseada em princípios SOLID e Clean Architecture, que são conceitos de design de software que ajudam a criar sistemas mais robustos e fáceis de manter.

![Imagem venv](static/Estrutura-IJR.png)

Agora, vamos explicar cada parte dessa estrutura:

#### 6.1.1 .env e .gitignore
Ao compartilharmos o código do projeto, seja pelo GitHub ou por outro meio, não queremos compartilhar informações sensíveis, como senhas, chaves de API ou chaves de criptografia. Para isso, usamos um arquivo `.env` para armazenar essas informações e um arquivo `.gitignore` para ignorar esse arquivo ao enviar o código para o repositório no GitHub.

No arquivo `.env`, você pode definir variáveis de ambiente que serão usadas pelo seu código. Por exemplo:
```
MONGO_PWD=senha123
MONGO_USER=usuario123
```
No arquivo `.gitignore`, você deve adicionar o nome do arquivo `.env` para que ele não seja enviado para o repositório:
```
.env
```

E no seu código, você pode usar uma biblioteca como `python-dotenv` para carregar essas variáveis de ambiente:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PWD = os.getenv("MONGO_PWD")

# Conexão com o MongoDB usando as variáveis de ambiente
connect(db="todo_app", host=f"mongodb+srv://{MONGO_USER}:{MONGO_PWD}@cluster.mongodb.net/todo_app?retryWrites=true&w=majority")
```

Além disso, o arquivo `.gitignore` também é usado para ignorar outros arquivos que não queremos enviar para o repositório, como arquivos temporários, logs, arquivos muito grandes(banco de dados ou amostras), .venv, etc. Por exemplo:
```
.venv/
*.log # Ignora todos os arquivos que terminam com .log
*.tmp
```

#### 6.1.2 entities/
Na pasta `entities`, você define as entidades do seu sistema, que são os modelos de dados que representam os objetos do seu domínio. Por exemplo, no caso de uma aplicação que possua diferentes tipos de usuários, você poderia ter uma entidade `Admin` que define os campos que um administrador possui.

Exemplo de uma entidade `Admin.py`:
```python
import dotenv
from pydantic import BaseModel
from typing import Literal

dotenv.load_dotenv()

class Admin(BaseModel):
    _id: str
    name: str
    email: str
    password: str
    
    reset_pwd_token : str = ""
    reset_pwd_token_sent_at : int = 0
```

#### 6.1.3 middlewares/
Na pasta `middlewares`, você define os middlewares que serão usados na sua aplicação. Middlewares são funções que interceptam as requisições e respostas da sua aplicação, permitindo que você execute código antes ou depois de uma rota ser executada. Isso é util principalmente para autenticação e autorização, mas também pode ser usado para logging, manipulação de erros, etc.

#### 6.1.4 models/
Na pasta `models`, você define os modelos de dados que serão salvos no banco de dados. Esses modelos são usados para mapear as entidades do seu sistema para os documentos do banco de dados.
A diferença entre entidades e modelos é que as entidades são usadas para definir a estrutura dos objetos do seu domínio, ou seja, o que eles representam e quais campos eles possuem, enquanto os modelos são usados para definir como esses objetos serão salvos no banco de dados, ou seja, como eles serão serializados e desserializados.
Ocorre a separação entre entidades e modelos para que você possa ter uma camada de abstração entre o domínio do seu sistema e a persistência dos dados. Isso permite que você mude a forma como os dados são armazenados sem afetar a lógica do seu sistema.
Exemplo de um modelo `AdminModel.py`:
```python
from mongoengine import *

class AdminModel(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    permission = StringField(required=True)
    
    reset_pwd_token = StringField(default="")
    reset_pwd_token_sent_at = IntField(default=0)

```

#### 6.1.5 repositories/
Na pasta `repositories`, você define os repositórios que serão usados para acessar os dados do banco de dados. Repositórios são classes que encapsulam a lógica de acesso aos dados, permitindo que você execute operações de CRUD(Create, Read, Update, Delete) de forma mais organizada e reutilizável. Em outras palavras, nos repositórios você define as funções que serão usadas para acessar os dados do banco de dados, como buscar um usuário pelo ID, buscar todos os usuários, criar um novo usuário, etc.

Exemplo de um repositório `AdminRepository.py`:
```python
import os
import bcrypt
import dotenv
from mongoengine import *
from cryptography.fernet import Fernet
from entities.admin import Admin
from models.admin_model import AdminModel
from models.fields.sensivity_field import SensivityField
from bson import ObjectId

class AdminRepository:
    fernet = Fernet(os.getenv("FERNET_SECRET_KEY"))

    def save(self, admin: Admin) -> None:
        admin_model = AdminModel()
        admin_dict = admin.model_dump()

        for k in AdminModel.get_normal_fields():
            if (k not in admin_dict):
                continue

            admin_model[k] = admin_dict[k]

        for k in AdminModel.sensivity_fields:
            admin_model[k] = SensivityField(fernet=self.fernet, data=admin_dict[k])

        admin_model.password = bcrypt.hashpw(f'{admin.password}'.encode(), bcrypt.gensalt()).decode()

        admin_model.save()
        
        admin._id = str(admin_model.id)

        return None
    
    def find_all(self) -> list[AdminModel]:
        return AdminModel.objects()
    
    def update(self, admin_id: str, updated_data: dict) -> None:
        try:
            admin_id = ObjectId(admin_id)
        except Exception:
            raise ValueError("Diretor ID inválido. Deve ser uma string hexadecimal de 24 caracteres.")

        admin_model = AdminModel.objects.with_id(admin_id)
        
        if not admin_model:
            raise ValueError("Diretor não encontrado")

        for key, value in updated_data.items():
            if hasattr(admin_model, key):
                setattr(admin_model, key, value)

        admin_model.save()

    def delete(self, admin_id: str) -> None:
        try:
            admin_id = ObjectId(admin_id)
        except Exception:
            raise ValueError("Diretor ID inválido. Deve ser uma string hexadecimal de 24 caracteres.")

        admin_model = AdminModel.objects.with_id(admin_id)

        if not admin_model:
            raise ValueError("Diretor não encontrado")

        admin_model.delete()

        return None
```

Perceba que em ao criar um novo usuario, nós usamos o bcrypt para criptografar a senha do usuário antes de salvá-la no banco de dados. Isso é importante para garantir a segurança das senhas dos usuários, já que mesmo que o banco de dados seja comprometido, as senhas não estarão em texto claro.
Além disso, perceba que em métodos como `save`, `update` e `delete`, erros são tratados e lançados como exceções. Isso é importante para garantir que o código seja robusto e fácil de depurar, já que você pode capturar essas exceções e tratá-las de forma adequada na sua aplicação. Sempre que for desenvolver uma rota ou função, tente pensar em possíveis erros que podem ocorrer e como evitá-los ou tratá-los. 

> **Atenção:** Pesquise mais sobre o bcrypt e como ele funciona, pois é um conceito importante de segurança que você deve entender tanto nesse exemplo como em todos os projetos que você vai fazer. Além disso, perceba que a chave de criptografia usada pelo Fernet(Procure o que é o Fernet) é armazenada em uma variável de ambiente, assim como é feito com todas as informações sensíveis do projeto como visto anteriormente.

#### 6.1.6 use_cases/
Na pasta `use_cases`, você define os casos de uso do seu sistema, que são as regras de negócio que definem como as entidades e repositórios interagem entre si. Nela, existem pastas para cada entidade do sistema e dentro de cada uma existem 2 tipos de arquivos:
- **algum_use_case.py**: Esse arquivo define as regras de negócio que serão executadas quando uma rota for acessada. Por exemplo, no caso de um usuário que deseja se cadastrar, você poderia ter um caso de uso `CreateUserUseCase` que define as regras de negócio para criar um novo usuário, como validar os dados do usuário, verificar se o email já está cadastrado, etc.
- **index.py**: Aqui você define quais rotas chamam cada caso de uso. Por exemplo, no caso de um usuário que deseja se cadastrar, você poderia ter uma rota `/users` que chama o caso de uso `CreateUserUseCase`.

Exemplo de um caso de uso `get_all_collaborators_use_case.py`:
```python
from repositories.sql_repositories.sql_collaborators_repository import SQLCollaboratorsRepository

class GetAllCollaboratorsUseCase:
    def __init__(self, sql_collaborators_repository: SQLCollaboratorsRepository):
        self.sql_collaborators_repository = sql_collaborators_repository

    def execute(self):
        return self.sql_collaborators_repository.get_colaboradores()
```

Exemplo de um arquivo `index.py` que define as rotas que chamam o caso de uso:
```python
from repositories.sql_repositories.sql_collaborators_repository import SQLCollaboratorsRepository
from fastapi import APIRouter, Depends, Response, Request
from use_cases.admin.collaborators.get_all_collaborators.get_all_collaborators_use_case import GetAllCollaboratorsUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

sql_collaborators_repository = SQLCollaboratorsRepository()
get_all_collaborators_use_case = GetAllCollaboratorsUseCase(sql_collaborators_repository=sql_collaborators_repository)

@router.get("/collaborators", dependencies=[Depends(validate_admin_auth_token)])
async def get_all_collaborators(request: Request, response: Response):
    """
    Get all collaborators.
    """
    collaborators = get_all_collaborators_use_case.execute()
    return {"collaborators": collaborators}
```

#### 6.1.7 config/
Na pasta `config`, você pode definir algumas configurações globais do seu sistema, como a conexão com o banco de dados ou com o frontend.

#### 6.1.8 main.py
O arquivo `main.py` é o ponto de entrada da sua aplicação. Nele, você vai importar as rotas definidas nos arquivos `index.py` de cada entidade e inicializar o FastAPI.
```python
from fastapi import FastAPI
from mongoengine import connect
from fastapi.middleware.cors import CORSMiddleware
import os
import glob
import dotenv
from importlib import import_module

dotenv.load_dotenv()

connect(host=f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PWD')}@blablabla.mongodb.net/")

app = FastAPI()

@app.get("/")
def test():
    return {"status": "OK v2 (3)"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

working_directory = os.path.dirname(os.path.abspath(__file__))
use_cases_directory = os.path.join(working_directory, "use_cases")
routes = glob.glob(os.path.join(use_cases_directory, "**/index.py"), recursive=True)

for route in routes:
    relative_path = os.path.relpath(route, working_directory)
    module_name = os.path.splitext(relative_path)[0].replace(os.path.sep, '.')

    try:
        print(f"Importing module: {module_name}")
        module = import_module(module_name)
        if hasattr(module, 'router'):
            app.include_router(module.router)
    except ModuleNotFoundError as e:
        print(f"Erro ao importar módulo {module_name}: {e}")
```

Perceba que logo no início do arquivo configuramos o CORS(Cross-Origin Resource Sharing), que é uma configuração de segurança que permite que o frontend acesse a API. Isso é importante para evitar problemas de segurança e garantir que apenas o frontend autorizado possa acessar a API, imagina se qualquer pessoa pudesse fazer requisições para a sua API? Isso seria um problema de segurança, certo? Por isso, é importante configurar o CORS corretamente.

#### 6.1.9 Conclusão da estrutura
Agora que você ja conhece a estrutura de um projeto da Insper Jr., é interessante que você pegue um projeto real da Insper Jr. para analisar, rodar e fazer modificações(lógico que isso deve ser feito em um repositório separado, nunca no repositório original). Assim, você vai ver como tudo funciona na prática e vai conseguir entender melhor os conceitos apresentados aqui.

Além disso, pesquise o que são os princípios SOLID e Clean Architecture e tente relacionar com a estrutura apresentada aqui. Esses conceitos são fundamentais para o desenvolvimento de software e vão te ajudar a escrever código mais limpo, organizado e fácil de manter.

### 6.2 Outros conceitos avançados
Além da estrutura apresentada acima, existem outros conceitos avançados que são importantes para o desenvolvimento web. Entretanto, esses conceitos não serão abordados aqui, mas é altamente recomendável que você pesquise e estude sobre eles, já que são conceitos que eles aparacem consatantemente em projetos reais. 
Eles são:
- **Autenticação e Autorização**: Entender como implementar autenticação de usuários e autorização de acesso a recursos é fundamental para qualquer aplicação web. Pesquise sobre JWT (JSON Web Tokens), isso é muito utilizado aqui na Insper Jr. 
- **Banco de dados relacionais**: Embora você tenha aprendido a usar o MongoDB, no mercado existem **muitos** sistemas que usam bancos de dados relacionais como MySQL, PostgreSQL e SQLite. Por isso, podem existir projetos da Insper Jr. que você talvez tenha que integrar algum banco de dados do cliente que seja relacional. ** Durante o semestre, vai ocorrer uma trilha de conceitos avançados de desenvolvimento web, que vai introduzir SQL e banco de dados relacionais.**
- **Deploy**: Depois de desenvolver uma aplicação, como coloco ela no ar? Existem várias opções de deploy, como Heroku, AWS, DigitalOcean, entre outras. Pesquise sobre como fazer o deploy de uma aplicação FastAPI e uma aplicação React.
- **Documentação**: Documentar a API é fundamental para que outros desenvolvedores possam entender como usá-la, tanto para um colega que possa entrar no projeto quanto para o cliente que vai usar e manter a API. O FastAPI já gera uma documentação interativa automaticamente usando o Swagger, que pode ser acessada em `http://localhost:8000/docs`. Entretanto, é interessante que você aprenda a documentar suas rotas e modelos de dados de forma mais detalhada, para que outros desenvolvedores possam entender como usá-las corretamente. Para isso, consulte a [documentação do FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) e veja como documentar suas rotas e modelos de dados. (Isso aqui é chato de fazer mas é bem fácil)

