-- test the whole project --

what you need installed:
docker
node js
react app

1. pull version from main to your local ide (vscode, pycharm,...)
2. open terminal in ide and enter command: docker compose up --build
3. go to django gunicorn container and create the first admin user:
3.1 type into django gunicorn container console: python3 manage.py createsuperuser
4. clone from frontend branch into new project
5. in new project navigate to directory frontend in terminal
6. type into terminal: npm start
7. you should see the frontend opening itself in the browser