# Clube de Leitura - Backend

API REST do **Clube de Leitura**, trabalho 2 da disciplina INF1407 (Programação para
Web - PUC-Rio). O backend é uma API JSON feita com **Django REST Framework**, com
autenticação **JWT** e documentação **Swagger/OpenAPI**. O frontend é um projeto
separado (site estático em HTML/CSS/TypeScript) que consome esta API.

- Repositório do frontend: https://github.com/guilhermesenko/frontend_t2

## Tecnologias

- Python 3.12 / Django + Django REST Framework
- `djangorestframework-simplejwt` - autenticação JWT (access + refresh)
- `drf-spectacular` - documentação Swagger / OpenAPI
- `django-cors-headers` - CORS (o frontend roda em outra origem)
- PostgreSQL (produção, via Docker) / SQLite (desenvolvimento)
- gunicorn + whitenoise (servir em container)

## Domínio

- **Livro** - catálogo de livros (CRUD restrito a administradores; leitura pública).
- **Leitura** - lista de leituras pessoal de cada usuário (status *Quero Ler / Lendo /
  Li*, nota de 1 a 5 e resenha), protegida por usuário.

## Como rodar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd ClubeLeitura
python manage.py migrate
python manage.py createsuperuser      # opcional, para acessar o /admin
python manage.py runserver
```

A API sobe em `http://localhost:8000/`. Sem a variável de ambiente `DB_HOST` o
projeto usa SQLite automaticamente.

## Rodando com Docker (Django + PostgreSQL)

```bash
docker compose up --build
```

Sobe o PostgreSQL e o backend em `http://localhost:8000/`.

## Documentação da API

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- Schema OpenAPI: `http://localhost:8000/api/schema/`

## Autenticação (JWT)

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/api/token/` | login - retorna `access` e `refresh` |
| POST | `/api/token/refresh/` | renova o `access` |
| POST | `/api/token/verify/` | verifica um token |

Envie o token nas requisições protegidas no cabeçalho
`Authorization: Bearer <access token>`.

## Endpoints da aplicação

### Livros (catálogo)
| Método | Rota | Permissão |
| --- | --- | --- |
| GET | `/livros/` | pública |
| POST | `/livros/` | admin (is_staff) |
| GET | `/livros/<id>/` | pública |
| PUT | `/livros/<id>/` | admin |
| DELETE | `/livros/<id>/` | admin |

### Leituras (lista pessoal, sempre do usuário logado)
| Método | Rota | Permissão |
| --- | --- | --- |
| GET | `/leituras/` | autenticado |
| POST | `/leituras/` | autenticado |
| GET | `/leituras/<id>/` | autenticado (dono) |
| PUT | `/leituras/<id>/` | autenticado (dono) |
| DELETE | `/leituras/<id>/` | autenticado (dono) |

### Contas
| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/contas/registrar/` | cria uma conta |
| GET | `/contas/whoami/` | dados do usuário logado |
| PUT | `/contas/trocar-senha/` | troca a senha (autenticado) |
| POST | `/contas/recuperar-senha/` | solicita token de redefinição |
| PUT | `/contas/recuperar-senha/` | redefine a senha com uid + token |

Em desenvolvimento, a redefinição de senha usa o `EMAIL_BACKEND` de console: o uid e
o token aparecem no log do servidor.

## Status

Funcionalidades implementadas: CRUD de livros e de leituras, autenticação JWT,
registro de usuário, troca e redefinição de senha, controle de acesso por papel
(admin x usuário) e documentação Swagger de todos os endpoints.
