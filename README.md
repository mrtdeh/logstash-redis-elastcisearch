# logstash-redis-elasticsearch

This is a test project to work in logstash + redis + elasticsearchhosted on docker, first of all Python app Fetch data from ```access.log``` from the selected Repo Log (nginx / apache2) and convert it to JSON, store it to Redis and then the rest of the story.

This directory contains a docker-compose.yml that will allow you to quickly spin up linked & configured containers running these applications:

   - python app (fetch and convert logs to json)
   - redis
   - logstash
   - elasticsearch

## Requirement

    docker
    docker-compose

## Quickstart

### Config

first you must config app for read source by change enviroment variable in ```docker-compose.yml``` to ``` nginx ``` or ``` apache2 ```:

```
.
.
    app:
        .
        .
	environment: 
            - Log_Source=/var/log/[nginx/apache2]/access.log
	.
	.
.
.
```

### Starting

start all services with ```docker-compose up -d``` and docker will download requirement images and build all of them.
### Checking

only run ```docker-compose logs -f``` to show logs from containers .
### Updating

if you changed the source run ```docker-compose up -d --build``` to rebuild containers which want to change.
### How it works?

first, python app fetch real-time ```access.log``` file from the default path from ```/var/log/[nginx/apache2]``` and convert all rows to json records, then append this records one-by-one in the redis as a list of json,

second, logstash run a input event for getting json's from redis and magic it,and out that to the elasticsearch for processing.
In the future

    - implement clustering for elasticsearch and redis.

