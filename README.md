
# Todo List Microservice

## Descrição
Este projeto é um microserviço para gerenciar uma lista de tarefas, desenvolvido com FastAPI, PostgreSQL e Redis, e containerizado usando Docker. Ele permite criar, ler, atualizar e deletar tarefas, armazenando os dados no PostgreSQL e utilizando o Redis para caching.

## Tecnologias Utilizadas
- **FastAPI**: Framework web para a criação de APIs.
- **PostgreSQL**: Banco de dados relacional.
- **Redis**: Banco de dados em memória utilizado para caching.
- **Docker**: Ferramenta para containerização.
- **pytest**: Framework de testes para Python.
- **httpx**: Cliente HTTP para testar a API.
- **Kubernetes**: Sistema de orquestração de contêineres.

## Estrutura do Projeto
- `app/`
  - `main.py`: Aplicação principal do FastAPI.
  - `database.py`: Configuração do banco de dados.
  - `models.py`: Definição dos modelos do SQLAlchemy.
  - `schemas.py`: Definição dos esquemas do Pydantic.
- `routers/`
  - `tasks.py`: Rotas para gerenciar tarefas.
- `endpoints/`
  - `task.py`: Funções de manipulação das tarefas.
- `docker-compose.yml`: Configuração dos serviços Docker.
- `Dockerfile`: Definição da imagem Docker para a aplicação.
- `init-db.sh`: Script para inicialização do banco de dados.
- `wait-for-postgres.sh`: Script para esperar o PostgreSQL iniciar.
- `tests/`: Testes automatizados para a aplicação.
  - `test_task.py`: Testes das funcionalidades de tarefas.
- `requirements.txt`: Dependências do projeto.
- `k8s/`: Manifests do Kubernetes.
  - `namespace.yml`: Definição do namespace.
  - `postgres-deployment.yml`: Deployment e Service do PostgreSQL.
  - `redis-deployment.yml`: Deployment e Service do Redis.
  - `todo-list-app-deployment.yml`: Deployment e Service da aplicação.

## Pré-requisitos
- Docker e Docker Compose instalados.
- Python 3.12.4 e pip instalados.
- Minikube instalado para rodar o Kubernetes localmente.

## Configuração e Execução

### 1. Clone o Repositório
```sh
git clone https://github.com/usuario/todo-list-microservice.git
cd todo-list-microservice
```

### 2. Configure e Inicie os Contêineres Docker
```sh
docker-compose up --build
```

Isso irá:
- Iniciar um contêiner com PostgreSQL.
- Iniciar um contêiner com Redis.
- Construir e iniciar o contêiner da aplicação FastAPI.

### 3. Acesse a Aplicação
A aplicação estará disponível em [http://localhost:8000](http://localhost:8000).

### 4. Executando Testes
Para rodar os testes automatizados, execute:
```sh
pytest tests/test_task.py
```

## Endpoints da API

### Criar uma Tarefa
- **POST** `/tasks/`
  - Exemplo de Corpo de Requisição:
    ```json
    {
      "title": "Test Task",
      "description": "Test Description"
    }
    ```
  - Resposta de Sucesso:
    ```json
    {
      "id": 1,
      "title": "Test Task",
      "description": "Test Description",
      "completed": false
    }
    ```

### Ler uma Tarefa
- **GET** `/tasks/{id}`
  - Resposta de Sucesso:
    ```json
    {
      "id": 1,
      "title": "Test Task",
      "description": "Test Description",
      "completed": false
    }
    ```

### Atualizar uma Tarefa
- **PUT** `/tasks/{id}`
  - Exemplo de Corpo de Requisição:
    ```json
    {
      "title": "Updated Task",
      "description": "Updated Description",
      "completed": true
    }
    ```
  - Resposta de Sucesso:
    ```json
    {
      "id": 1,
      "title": "Updated Task",
      "description": "Updated Description",
      "completed": true
    }
    ```

### Deletar uma Tarefa
- **DELETE** `/tasks/{id}`
  - Resposta de Sucesso:
    ```json
    {
      "message": "Task deleted successfully"
    }
    ```

## Detalhes dos Arquivos de Configuração

### docker-compose.yml
Define os serviços para PostgreSQL, Redis e a aplicação FastAPI.

### Dockerfile
Define a imagem Docker para a aplicação.

### wait-for-postgres.sh
Script para esperar a inicialização do PostgreSQL.

### init-db.sh
Script para inicializar o banco de dados.

## Kubernetes
Manifests do Kubernetes para orquestração dos serviços.

### namespace.yml
Define o namespace `todo-list`.

### postgres-deployment.yml
Deployment e Service para o PostgreSQL.

### redis-deployment.yml
Deployment e Service para o Redis.

### todo-list-app-deployment.yml
Deployment e Service para a aplicação FastAPI.

## Testes Automatizados
O arquivo de testes `tests/test_task.py` garante que todas as funcionalidades do CRUD estão funcionando corretamente.

## Deployment no Railway
Este projeto pode ser facilmente implantado no Railway, uma plataforma de hospedagem de fácil uso.

### Configuração do Railway
1. **Clone o Repositório:**
    ```sh
    git clone https://github.com/usuario/todo-list-microservice.git
    cd todo-list-microservice
    ```

2. **Crie um Novo Projeto no Railway:**
    - Acesse o [Railway](https://railway.app) e crie uma nova conta ou faça login.
    - Clique em "New Project" e selecione "Deploy from GitHub repo".
    - Conecte seu repositório GitHub ao Railway.

3. **Configure as Variáveis de Ambiente:**
    - No dashboard do Railway, vá para a seção "Settings" do seu projeto.
    - Adicione as seguintes variáveis de ambiente:
      - `DATABASE_URL`: URL de conexão do PostgreSQL.
      - `REDIS_URL`: URL de conexão do Redis.
    - Você pode encontrar essas URLs nas configurações de cada serviço no Railway.

4. **Deploy:**
    - Clique em "Deploy" no Railway.
    - A aplicação será construída e implantada automaticamente.

### Acesse a Aplicação
A aplicação estará disponível em uma URL fornecida pelo Railway, por exemplo, `https://your-project-name.up.railway.app`.

Com essas etapas, você terá seu microserviço Todo List implantado no Railway, pronto para uso.
