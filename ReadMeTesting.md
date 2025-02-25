Instructions for manually testing frontend

1. pull project from main
2. create files in root directory:

envvarsdb.env:
```
POSTGRES_USER='Caro'
POSTGRES_PASSWORD='password'
POSTGRES_DB='test_db'
PGADMIN_DEFAULT_EMAIL='Caro@admin.com'
PGADMIN_DEFAULT_PASSWORD='root'
```

envvarsdjango.env:
```
SECRET_KEY=yz^ym!prbpmq^s!mcx@@5x)sa4#p7(w1k_v31po@ljt2%u%q6%
NAME='test_db'
USER= 'Caro'
PASSWORD= 'password'
HELMHOLTZ_CLIENT_ID='PSE_Lastenkarle'
HELMHOLTZ_CLIENT_SECRET='67gqJ!#ALJnf*hU*dkcc'
EMAIL_HOST_USER= 'buchungssystem_lastenkarle@mail.de'
EMAIL_HOST_PASSWORD= 'uHzF8OWcl8G5XVaCGF5l'
CANONICAL_HOST='http://localhost'
```

3. run in root directory of project: docker compose up --build
4. in the django-gunicorn-1 container go to terminal and run command: `python3 manage.py createsuperuser`
5. go to <http://localhost:3000>
6. login in with credentials from createsuperuser or register new account
