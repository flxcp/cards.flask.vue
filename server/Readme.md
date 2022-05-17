## Cards &middot; [![CodeQL](https://github.com/flxhq/cards.flask.vue/actions/workflows/codeql.yml/badge.svg)](https://github.com/flxhq/cards.flask.vue/actions/workflows/codeql.yml)

This folder contains Python and other Files for Server.

### External Softwares.
1. Redis DB
2. [MailHog](https://github.com/mailhog/MailHog)

### Configurations

> Default configurations can be found in `app/config.py` file. Update them as required.

### Packages.

- Flask
- Flask-Caching
- Flask-RESTful
- Flask-Security
- Flask-CORS
- Jinja
- Weasyprint
- Celery
- Redis

### Instructions to run the app
#### Project Setup

```bash
pipenv install
```

#### Run the Server

```bash
gunicorn main:app
```

#### Start Celery beat for periodic task

```bash
celery -A main.celery beat --max-interval 1 -l info
```

#### Run Celery Workers.

```bash
celery -A main.celery worker -l info
```

#### Login Credentials
```
username: admin@cards.com
password: password
```

Finally, Development Server is up at [http://localhost:5000](http://localhost:5000).


#### Security

 Configure CORS for secure usage.