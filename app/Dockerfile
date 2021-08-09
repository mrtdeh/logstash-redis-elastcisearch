FROM python:3-alpine

WORKDIR /usr/src/app

RUN pip install redis pyinotify

COPY . .

CMD [ "python", "-u", "./app.py" ]