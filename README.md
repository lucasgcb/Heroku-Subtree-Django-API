Fork com a solução de um desafio aberto da Instruct-BR. 
Repositório: https://github.com/instruct-br/teste-python-jr-remoto

## App na plataforma Heroku

https://voughzera.herokuapp.com/api/orgs/

API:

`/api/orgs/<login>`
onde `<login>` é o nome de login da organização no GitHub.

- GET retorna os dados da organização em json como descritos na [API oficial do GitHub](https://docs.github.com/en/rest/reference/orgs#get-an-organization)
- DELETE retorna um 204 se existir em cache, 404 se não.

`/api/orgs/`
- GET retorna os dados no seguinte formato:
 ```
    {
        "login": "string",
        "name": "string",
        "score": int
    }
 ```


Score é dado pela soma do número de membros públicos da organização com o número de repositórios públicos da organização.
Esta informação é utilizada para ordenar as organizações em cache, de maior prioridade para menor.


# Informações de Desenvolvimento

Utiliza [whitenoise](https://github.com/evansd/whitenoise) para entrega de arquivos estáticos.

### Rodar o projeto com docker-compose
```bash
docker-compose up
```

### Rodar o projeto com docker run louco
```bash
sudo docker run --network host -d $(sudo docker build --tag vough -q .)
```

### Comandos chave para desenvolvimento

```bash
### Git para enviar ao heroku; subtree pois o projeto é subpasta
heroku git:remote -a voughzera
git subtree push --prefix vough_backend heroku master 
git subtree split --prefix vough_backend -b voughtree
git push -f heroku voughtree:master

## Virtual Environment para requerimentos
python3.9 -m venv vough
source vough/bin/activate

## Bibliotecas para compilar psycopg2
sudo apt-get install python3.9-dev
sudo apt install libpq-dev

## Arquivos estaticos django
python manage.py collectstatic
gunicorn vough_backend.wsgi

## Rodar testes
k6 run -e API_BASE='http://localhost:8000/' tests-open.js
```
