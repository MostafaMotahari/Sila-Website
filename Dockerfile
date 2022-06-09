FROM python:3.10

ENV DockerHOME=/home/djnago/sila
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME
COPY . $DockerHOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD gunicorn sila.wsgi