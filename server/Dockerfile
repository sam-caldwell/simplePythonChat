FROM ubuntu:latest

COPY app.py /opt/
COPY static /opt/
COPY templates /opt/
COPY entrypoint.sh /opt/
COPY requirements.txt /opt/


RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python3 python3-pip -y && \
    pip3 install -r /opt/requirements.txt

WORKDIR /opt/

ENTRYPOINT [ "/opt/entrypoint.sh" ]

CMD [ "/opt/entrypoint.sh" ]
