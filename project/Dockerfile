FROM python:3.10.6-slim
WORKDIR /usr/src/project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r ./backend/app/requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "-m", "./backend/app/app" ]