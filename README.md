# Customer Accounts Service

[![Build Status](https://github.com/abdymomynshyngys281-blip/g/accounts/actions/workflows/ci-build.yaml/badge.svg)](https://abdymomynshyngys281-blip/g/accounts/actions)

Customer Accounts microservice: REST API (Flask) with CRUD for accounts,
Talisman security headers, CORS, CI on GitHub Actions, Docker/Kubernetes
deployment and a Tekton CD pipeline.

## Endpoints

| Method | URL | Description |
|---|---|---|
| POST | /accounts | Create an account |
| GET | /accounts | List accounts |
| GET | /accounts/{id} | Read an account |
| PUT | /accounts/{id} | Update an account |
| DELETE | /accounts/{id} | Delete an account |
| GET | /health | Health check |

## Development

```bash
pip install -r requirements.txt
nosetests          # tests + coverage (Python 3.9)
flake8 service
flask run          # or: gunicorn --bind 0.0.0.0:8080 service:app
```
