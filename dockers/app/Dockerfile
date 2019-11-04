#### PRODUCTION
#FROM isard/alpine-pandas:latest AS production
FROM alpine:latest AS production
MAINTAINER isard <info@isard.com>

# Needed in hypervisor connection scripts
RUN apk add --no-cache bash curl openssh-client

# Removed in new version. Kept here only to reference
#py3-libvirt py3-paramiko py3-lxml py3-pexpect py3-openssl py3-bcrypt py3-gevent py3-netaddr py3-requests curl openssh-client py3-psycopg2

COPY dockers/app/requirements.pip3 /requirements.pip3
RUN apk add --no-cache --virtual .build_deps build-base python3-dev
RUN pip3 install --no-cache-dir -r requirements.pip3
RUN apk del .build_deps

RUN mkdir -p /root/.ssh
RUN echo "Host isard-hypervisor \
	StrictHostKeyChecking no" >/root/.ssh/config
RUN chmod 600 /root/.ssh/config

RUN apk add --no-cache supervisor
RUN mkdir -p /var/log/supervisor
COPY dockers/app/supervisord.conf /etc/supervisord.conf

# GRPC SERVER
EXPOSE 1313

COPY dockers/app/certs.sh /
COPY dockers/app/add-hypervisor.sh /

RUN mkdir /isard
ADD ./src /isard
RUN mv /isard/isard.conf.docker /isard/isard.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]


#### DEVELOPMENT
FROM production AS development
RUN apk add --no-cache git vim nano openssh 
#py3-xmltodict
RUN apk add --no-cache build-base python3-dev
RUN pip3 install ipython pytest grpcio-tools


#COPY dockers/app/certs_devel.sh /certs.sh
CMD /usr/bin/supervisord -c /etc/supervisord.conf
