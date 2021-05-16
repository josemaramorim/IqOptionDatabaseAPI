FROM python:3.8-slim-buster

WORKDIR /srv

RUN apt update && apt upgrade -y

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

# ADD Pipefiles
ADD Pipfile Pipfile.lock ./

# INSTALL FROM Pipefile.lock FILE
RUN pip install --no-cache -U pip pipenv && pipenv install --system

# ADD APP
ADD . .

EXPOSE 80

# ENTRYPOINT
ENTRYPOINT ["gunicorn", "src.app:app", "-c", "./src/gunicorn.py"]
