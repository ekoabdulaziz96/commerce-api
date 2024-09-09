# apps

apps for create REST-API

[![Code](https://img.shields.io/badge/Code-Python-1B9D73?style=flat&logo=python)](https://python.org)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT


## How to run
Make sure you already installed **python3.12** or higher in your machine

1. Create your virtualenv and activate (if you are using virtuanenv)
2. Move your current root path to this project
    ```sh
    cd commerce-api
    ```
3. Install library 
    ```sh
    # for development purpose
    pip install -r ./requirements/local.txt
    ```
4. make .env file, you can duplicate it from .env.dev and rename it to .env
    - you can edit the value for your own environment IP/port or something else
    - recommend to use same environment with author, we use docker that inclue `PostgreSQL, Adminer, Redis`
    - step to run container docker
        ```sh
        # change directory to xsources
        cd xsources

        # run docker compose
        docker-compose -f .\postgres_redis.yml up -d
        ```
    - step to turn off container docker
        ```sh
        # turn off docker compose
        docker-compose -f .\postgres_redis.yml down
        ```
    - make sure the DB is already created, 
        - you can open adminer in your browser with url `http://localhost:8080/`
        - login with credential:
            - sistem = PostgreSQL
            - server = postgresDocker
            - pengguna = postgres
            - sandi = postgres
        - check the the DB `db_core_notification` is exist or not, 
            - you can create it, if not exist
5. run migraton file
    ```sh
    python manage.py migrate
    ```
6. create your superuser
    ```sh
    python manage.py createsuperuse
    ```
7. run server
    ```sh
    python manage.py runserver 8000
    ```
8. run server celery worker
    ```sh
    # create new terminal and activate the virtualenv
    # make sure, you are in the root project
    celery -A config.celery_app worker -l info

    # celery worker on windows user, `--pool solo`
    celery -A config.celery_app worker --pool solo -l INFO
    ```

9. run server celery beat (scheduler)
    ```sh
    # create new terminal and activate the virtualenv
    # make sure, you are in the root project
    # caution, please run celery worker first

    celery -A config.celery_app beat
    ```
10. consume endpoint
    - you can see the api-contract in, url: {base_url}/api/docs/
    - If you want to use `postmant`, you can import my collection in folder `xsources`
    - sample csv file for product, you can find it in folder `xsources`

11. access CMS with superuser, url: `{base_url}/admin/`
    
<br>

### Need to know
- postmant collection in folder `xsources`
- we use Api-Secret key in header for simple authenticate (check the postmant collection)
- you can read more, about api explanation in note.txt folder `xsources`
<br>

## How to set connection DB
Set your .env file for variable key for `SQLALCHEMY_DATABASE_URI` 
<br> ex : `SQLALCHEMY_DATABASE_URIL="postgresql://username:password@host:port/db_name"`
<br><br>

## Unittest & Coverage
all of unit test all saved in `./tests/*` folder. 

1. Run Unittest (using pytest)
<br>You can run unittest by executing this command 
    ``` sh
    # run all unittest
    pytest tests

    # run specific unittest
    # pytest tests/package/moduleName.py::className::functionName
    # ex:
    pytest tests/test_server.py::TestServer::test_case_1
    ```
2. Coverage
    ``` sh
    # run all test
    # you can skip module/file in .coveragerc file
    coverage run --source='.' --rcfile='.coveragerc' -m pytest

    # make report
    coverage report

    # make html report
    coverage html
    # follow the generated htmlcov path and open it in browser
    # ex: Wrote HTML report to `htmlcov\index.html`
    ```
<br>

## Linting & Formatter
Ruff re-implements some of the most popular Flake8 plugins and related code quality tools (include: isort)
```sh
#  LINTING
# check the code first
ruff check .

# auto fix 
ruff check --fix

# ignore check , add this comment after last code `# noqa`
# ex: a = 1   # noqa
```

Auto Formatter with Ruff
<br> The Ruff formatter is an extremely fast Python code formatter designed as a drop-in replacement for Black
 
```sh
# FORMATTER
ruff check --select I --fix   # run isort (to sorting the import)
ruff format

# ignore check , add this comment after last code `# fmt: skip`
# ex: a = 1   # fmt: skip
```
<br>


## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd apps
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd apps
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd apps
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).


## Note:
- this project is created base on [Django cookiecuter]https://github.com/cookiecutter/cookiecutter-django)
- author: ekoabdulaziz96@gmail.com