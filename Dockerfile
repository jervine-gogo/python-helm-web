# Base on latest alpine image
FROM alpine
LABEL MAINTAINER="Jonathan Ervine <jonathan.ervine@gogox.com>"

# Install updates
ENV LANG='en_US.UTF-8' \
    LANGUAGE='en_US.UTF-8' \
    FLASK_APP=/data/app-dev/app.py \
    VERSION=1.1.4

RUN apk update && \
    apk -U upgrade --ignore alpine-baselayout && \
    apk -U add python3 gcc py3-pip python3-dev musl-dev libffi-dev git curl && \
    adduser -D python && \
    mkdir /data && cd /data && git clone --single-branch --branch SRE-622 https://github.com/jervine-gogo/python-helm-web /data && \
    pip3 install -r /data/requirements.txt && \
    curl -L https://get.helm.sh/helm-v2.13.1-linux-amd64.tar.gz -o /tmp/helm-2.13.1.tgz && \
    tar -zxvf /tmp/helm-2.13.1.tgz --strip-components=1 -C /usr/local/bin linux-amd64/helm && \
    rm -rf /tmp/src && rm -rf /var/cache/apk/* 

EXPOSE 3000

#USER python

CMD [ "/usr/bin/python3", "/data/main.py" ]
