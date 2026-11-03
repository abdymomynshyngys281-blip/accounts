# Пошаговый план: Devops Capstone (задания 1–33)

Файлы проекта уже готовы. Ваша часть: GitHub, Kanban, терминал лабораторной среды, скриншоты.
Замените `YOUR_GITHUB_USERNAME` в README.md на свой логин.

## 0. Репозиторий
1. На GitHub создайте **публичный** репо `accounts`, загрузите все файлы (ветка main).
2. Включите Actions (Settings → Actions → Allow all).
3. Создайте Kanban: Projects → New project → Board (колонки: New Issues, Ice Box, Product Backlog, Sprint Backlog, In Progress, Done) или ZenHub, если курс требует его.

## 1. Истории (создайте как Issues)
Ровно эти названия (скриншоты проверяют дословно):

| # | Название | Метка |
|---|---|---|
| 1 | Setting up the development environment | Technical Debt |
| 2 | Create an account in the service | Enhancement |
| 3 | Read an account from the service | Enhancement |
| 4 | List all accounts in the service | Enhancement |
| 5 | Update an account in the service | Enhancement |
| 6 | Delete an account from the service | Enhancement |
| 7 | Need the ability to automate continuous integration checks | Technical Debt |
| 8 | Need to add security headers and CORS policies | Technical Debt |
| 9 | Containerize your microservice using Docker | Technical Debt |
| 10 | Deploy your Docker image to Kubernetes | Technical Debt |
| 11 | Create a CD pipeline to automate deployment to Kubernetes | Technical Debt |

Названия 3, 5, 6 из заданий: "Read an account from the service", "Update an account in the service",
"Delete an account from the service", "List all accounts in the service". История создания: любое название.
Проверьте по тексту заданий 9–12, 20, 24, 27, 28, 33, что формулировки совпадают у вас 1 в 1.

## 2. Какое задание чем закрывается

| Задание | Что сдать | Как получить |
|---|---|---|
| 1 | URL README.md | `https://github.com/<user>/accounts/blob/main/README.md`; бейдж должен быть зелёным (после первого успешного Actions) |
| 2 | URL user-story.md | `.../blob/main/user-story.md` |
| 3 | `planning-userstories-done.png` | доска, колонка New Issues со всеми историями |
| 4 | `planning-productbacklog-done.png` | колонка Ice Box с историями |
| 5 | `planning-labels-done.png` | Product Backlog, видны метки Technical Debt / Enhancement |
| 6 | `planning-kanban-done.png` | Sprint Backlog: у каждой истории estimate и Sprint 1 |
| 7 | URL setup.cfg | `.../blob/main/setup.cfg` |
| 8 | `rest-techdebt-done.png` | "Setting up the development environment" в Done |
| 9 | `read-accounts.png` | "Read an account from the service" в Done |
| 10 | `list-accounts.png` | "List all accounts in the service" в Done |
| 11 | `update-accounts.png` | "Update an account in the service" в Done |
| 12 | `delete-accounts.png` | "Delete an account from the service" в Done |
| 13–17 | текстовые файлы curl | см. раздел 3 |
| 18 | `sprint2-plan.png` | Sprint Backlog второго спринта: 2 новые истории |
| 19 | `ci-workflow-done` | см. раздел 4 |
| 20 | `ci-kanban-done.png` | "Need the ability to automate continuous integration checks" в Done |
| 21 | URL ci-build.yaml | `.../blob/main/.github/workflows/ci-build.yaml` |
| 22 | URL service/__init__.py | `.../blob/main/service/__init__.py` |
| 23 | `security-headers-done` | `nosetests > security-headers-done 2>&1` |
| 24 | `security-kanban-done.png` | "Need to add security headers and CORS policies" в Done |
| 25 | `sprint3-plan.png` | 3 истории в Sprint 3 |
| 26 | `kube-app-output` | см. раздел 5 |
| 27 | `kube-docker-done.png` | "Containerize your microservice using Docker" в Done |
| 28 | `kube-kubernetes-done.png` | "Deploy your Docker image to Kubernetes" в Done |
| 29 | URL Dockerfile | `.../blob/main/Dockerfile` |
| 30 | `kube-images` | `docker images accounts > kube-images` |
| 31 | `kube-deploy-accounts` | раздел 5 |
| 32 | `pipelinerun.txt` | раздел 6 |
| 33 | `cd-pipeline-done.png` | "Create a CD pipeline..." в Done |

## 3. REST curl (задания 13–17)
Запустите сервис: `flask run --port 8080` (или `gunicorn --bind 0.0.0.0:8080 service:app`).
Talisman по умолчанию редиректит http на https. Для локальных curl запускайте с `FORCE_HTTPS=false`:
`FORCE_HTTPS=false gunicorn --bind 0.0.0.0:8080 service:app`.
Пример (команда + её вывод в один файл):

```bash
{ set -x; curl -i -X POST http://localhost:8080/accounts -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","address":"1 Main St","phone_number":"555-1234"}'; } > rest-create-done 2>&1
{ set -x; curl -i http://localhost:8080/accounts; } > rest-list-done 2>&1
{ set -x; curl -i http://localhost:8080/accounts/1; } > rest-read-done 2>&1
{ set -x; curl -i -X PUT http://localhost:8080/accounts/1 -H "Content-Type: application/json" \
  -d '{"name":"Jane Smith","email":"jane@example.com"}'; } > rest-update-done 2>&1
{ set -x; curl -i -X DELETE http://localhost:8080/accounts/1; } > rest-delete-done 2>&1
```

## 4. Задание 19 (ci-workflow-done)
Откройте последний зелёный запуск в Actions → скопируйте лог шагов (Checkout, Install dependencies, Lint, Run unit tests)
в файл `ci-workflow-done`.

## 5. Docker и Kubernetes (26, 30, 31)
```bash
docker build -t accounts:1 .
docker images accounts > kube-images
kubectl apply -f deploy/
kubectl port-forward svc/accounts 8080:8080     # откройте в браузере /accounts, сохраните JSON в kube-app-output
{ kubectl get all -l app=accounts; } > kube-deploy-accounts
```
(`kubectl get all` показывает deployment, pods, replicasets, service.)

## 6. Tekton (32)
```bash
kubectl apply -f tekton/pvc.yaml
kubectl apply -f tekton/tasks.yaml
kubectl apply -f tekton/pipeline.yaml
tkn pipeline start cd-pipeline -p repo-url="https://github.com/<user>/accounts.git" -p branch=main \
  -p build-image="image-registry.openshift-image-registry.svc:5000/$SN_ICR_NAMESPACE/accounts:latest" \
  -w name=pipeline-workspace,claimName=oc-lab-pvc --showlog
tkn pipelinerun logs --last > pipelinerun.txt
```
В лабе ClusterTask-и (git-clone, flake8, buildah, openshift-client) уже установлены; проверьте `tkn clustertask ls`.

## 7. Nose под Python 3.9
nose не работает на Python 3.10+. В лабе и CI используется 3.9 (Dockerfile и CI-файл уже так настроены).
Если локально Python новее, запускайте тесты через `python -m unittest discover -s tests -t .`.
