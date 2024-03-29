# TrackMe Ninja

[![GitHub Super-Linter](https://github.com/GirlsCodeBootCamp/trackme-python/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/GirlsCodeBootCamp/trackme-python/actions)

## About the application

TrackMeNinja identifies changes on the site you choose and alerts you on them. Don't spend time going through many sites yourself, leave it to TrackMeNinja

## Running on your machine

### Virtual environment

For better usability, you can install [Python virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) and work with the application in enclosed env

Install prerequisites

```bash
pip install -r requirements.txt
```

Run the application

```bash
python3 main.py
```

### Code Lint

CI/CD pipeline uses github/super-linter for linting the code. More information on [super-linter pages](https://github.com/github/super-linter/blob/main/docs/run-linter-locally.md)

```bash
docker pull github/super-linter:latest
docker run -e RUN_LOCAL=true -v ${PWD}:/tmp/lint github/super-linter
```

### Docker

Docker enables you to run application directly without a need to install and configure the environment. [Install Docker](https://docs.docker.com/engine/install/)

```bash
# build the image
docker build . -t trackme
# run the application
docker run --rm -it  -p 8000:8000/tcp trackme:latest
```

More documentation on Docker:

- [uvicorn Docker image](https://docker-fastapi-projects.readthedocs.io/en/latest/uvicorn.html)
- [Docker image with Uvicorn managed by Gunicorn for high-performance FastAPI web applications](https://pythonawesome.com/docker-image-with-uvicorn-managed-by-gunicorn-for-high-performance-fastapi-web-applications/)

### Compose

The web application will be available at [http://localhost](http://localhost)

To start the containers, use the following command:

```bash
docker-compose up
```

To check if the containers are running, use:

```bash
docker-compose ps
```

To rebuild all the containers, use the following command:

```bash
docker-compose up --build
```

To restart the web service, run:

```bash
docker-compose restart web
```

### Logs

To tail logs, run:

```bash
docker-compose logs -f web
```
