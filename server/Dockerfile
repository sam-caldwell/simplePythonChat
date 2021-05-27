FROM ubuntu:groovy-20210416

ENV MY_AUTH_SECRET="mysecret"

COPY app.py /opt/
COPY static /opt/
COPY templates /opt/
COPY entrypoint.sh /opt/
COPY requirements.txt /opt/

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python3 python3-pip -y && \
    pip3 install -r /opt/requirements.txt

RUN mkdir -p /opt/data/users && \
    echo "${MY_AUTH_SECRET}" > /opt/data/secret.dat

WORKDIR /opt/

ENTRYPOINT [ "/opt/entrypoint.sh" ]

CMD [ "/opt/entrypoint.sh" ]
