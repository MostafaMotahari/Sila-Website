FROM python:3.10

ENV DockerHOME=/home/djnago/sila
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME
COPY . $DockerHOME

RUN echo "[Unit]\n" \
        "Description=gunicorn daemon\n" \
        "After=network.target\n\n" \
        "[Service]\n" \
        "User=djnago\n" \
        "Group=www-data\n" \
        "WorkingDirectory=/home/djnago/sila\n" \
        "ExecStart=gunicorn --access-logfile - --workers 3 --bind unix:/home/djnago/sila/sila.sock sila.wsgi\n\n" \
        "[Install]\n" \
        "WantedBy=multi-user.target" > /etc/systemd/system/gunicorn.service

RUN systemctl start gunicorn

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD gunicorn sila.wsgi