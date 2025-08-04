# Mini-Rag

This is the minimal implementation of the Rag model for quesion answering


## Requirements 
- Python 3.8 or later 

#### Install python 

1) download python from [here](https://www.python.org/downloads/)
  - check add python path to system environment
2) create a new environment using the following command:
``` bash
$ python3 -m venv <envName>
```
3) Activate environment:
``` bash
$ source <envName>/bin/activate
```

## Initialization 

### 1) Install Required Packages
``` bash
$ pip install -r requirements.txt
```

### 2) Setup the environment variables
``` bash
$ cp .env.example .env
```
- set your `.env` variables

### 3) Setup Docker Environment Variables
``` bash
$cp ./docker/.env.example ./docker/.env
$cd docker
```
- set your `.env` variables for docker

## Install Docker
- Windows [here](https://docs.docker.com/desktop/setup/install/windows-install/)
- Linux [here](https://docs.docker.com/desktop/setup/install/linux/)

## Install MongoDB
### Use docker to run mongo or install it locally
1) Using Docker 
- ```bash
  $ docker compose -f /docker/docker-compose.yml up -d --build
  ```
2) Local Install 
- Install Mongo From [here](https://www.mongodb.com/docs/manual/installation/)

## Run FastAPI Server 
``` bash 
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```



