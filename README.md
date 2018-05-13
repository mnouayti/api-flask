# api flask

> flask api that synchronises pages with a chrome extension and a vuejs app, using 2 http requests Post and Get, built with flask-restful, mongodb, pymongo, marshmallow.   

## Endpoints


..* GET
all pages : http://0.0.0.0:500/api/pages
single page: http://0.0.0.0:5000/api/pages/id

..* POST
http://0.0.0.0:500/api/pages 

| params        | desc                 | type           |
| ------------- |:--------------------:| --------------:|
| html          | source code          | required       |
| url           | current tab url      | required       |
| title         | current tab title    | required       |
| creatd_by     | full name of the user| required       |
| creatd_at     | date of creation     | datetime.now() |
| id            | unique id of the page| str generated  |


## Prerequisites

In order to run the project in a local environment all you need is Docker and docker-compose tool installed.


## Building the project:

Go to the project directory where `docker-compose.yaml` and `Dockerfile` are located and run the command:

```bash
$ docker-compose build
```


## Running the server locally

You can run the project using docker-compose tool:

```bash
$ docker-compose up
```
