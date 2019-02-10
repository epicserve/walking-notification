FROM python:3.6.8

# Set the locale
RUN apt-get clean \
    && apt-get update \
    && apt-get install -y locales \
    && echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
    && locale-gen en_US.UTF-8

## ENVIRONMENT SETTINGS
ENV \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    USER=root \
    # This prevents Python from writing out pyc files \
    PYTHONDONTWRITEBYTECODE=1 \
    # This keeps Python from buffering stdin/stdout \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code

WORKDIR /code

COPY Pipfile Pipfile.lock ./

## Install Python Packages
RUN set -ex \
    && pip install pipenv --upgrade \
    && pipenv install --deploy --dev --system \
    && cp /etc/skel/.bashrc /root/.bashrc
