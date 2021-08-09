FROM python:3-alpine

ARG LOGSOURCE

WORKDIR /usr/src/app

RUN pip install redis pyinotify

ENV LOGSOURCE "$LOGSOURCE"

COPY . .

CMD [ "python", "-u", "./app.py" ]