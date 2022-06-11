FROM ubuntu:bionic
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update && apt install python3.10 -y && \
    apt-get -y install \
    python3.10-dev python3-pip python3.10-venv python3-wheel \
    libsqlclient-dev libssl-dev default-libmysqlclient-dev


ARG USER=root
USER $USER
RUN python3.10 -m venv venv
WORKDIR /app
COPY requirements.txt requirements.txt
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt

COPY . .
EXPOSE 5000
RUN chmod +x /app/start_server.sh
ENTRYPOINT ["./start_server.sh"]