FROM python:3.8-slim-buster

WORKDIR /app

RUN useradd -m -r ninja && \
    chown ninja /app

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

USER ninja

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

EXPOSE 80
ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ] 
