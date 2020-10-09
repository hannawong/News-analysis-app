# backend of xxswl 

> frame from: https://gitlab.secoder.net/example/monolithic-example

The backend was bootstrapped with [`django-admin startproject app`](https://docs.djangoproject.com/en/2.2/ref/django-admin/).
The frontend part was deleted.

## Usage

    docker build -t something .
    docker run --rm something

## Develop

### Structure

* __app__ Core settings for Django.
* __meeting__ Created by `python manage.py startapp meeting`.
* __manage.py__   settings for Django.

==the following files should remain unmodified==

* __pytest.ini__ Configuration for [pytest](https://docs.pytest.org/en/latest/).
* __requirements.txt__ Package manager with `pip`.
* __requirements_dev.txt__ Package manager with `pip`, including extra tools for development.
* **Dockerfile**  configure our docker image to run,  ' EXPOSE 80 '  set the port we can use
* **.gitlab-ci.yml**  configure  our CI/CD settings
* **sonar-project.properties**  configure  sonar 

### Tools

* `python manage.py runserver` Run this project in development mode.
* `python manage.py makemigrations` Detect changes in data schema.
* `python manage.py migrate` Apply migrations to current database.
* `pytest` Test.
* `pylint --load-plugins=pylint_django app meeting` Advanced [PEP8](https://www.python.org/dev/peps/pep-0008/) checking.

## License

MIT License
