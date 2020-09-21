# Base on latest alpine image
FROM debian:stable-slim
LABEL MAINTAINER="Jonathan Ervine <jonathan.ervine@gogox.com>"

# Install updates
ENV LANG='en_US.UTF-8' \
    LANGUAGE='en_US.UTF-8' \
    FLASK_APP=/data/app-dev/app.py \
    VERSION=1.1.4

RUN apt update && \
    apt install -y python3 gcc python3-pip python3-dev git curl && \
    adduser -D python && \
    mkdir /data && cd /data && git clone --single-branch --branch SRE-617 https://github.com/jervine-gogo/python-helm-web /data && \
    pip3 install -r /data/requirements.txt && \
    curl -L "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" -o /usr/local/bin/kubectl && \
    chmod 755 /usr/local/bin/kubectl && \
    curl -L https://get.helm.sh/helm-v2.13.1-linux-amd64.tar.gz -o /tmp/helm-2.13.1.tgz && \
    tar -zxvf /tmp/helm-2.13.1.tgz --strip-components=1 -C /usr/local/bin linux-amd64/helm && \

EXPOSE 3000

#USER python

CMD [ "/usr/bin/python3", "/data/main.py" ]
