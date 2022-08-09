FROM python:3.10.6-slim
WORKDIR /usr/src/project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib
RUN pip install --upgrade pip
COPY backend ./backend
RUN pip install -r ./backend/app/requirements.txt
