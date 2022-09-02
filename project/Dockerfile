FROM python:3.10.5
WORKDIR /usr/src/project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib
RUN pip install --upgrade pip
COPY backend ./backend
WORKDIR /usr/src/project/backend/app
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root