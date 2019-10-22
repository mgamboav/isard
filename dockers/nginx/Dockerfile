#### BUILD
FROM node:lts-alpine AS build

COPY ./src/new_webapp/frontend /app

WORKDIR /app
RUN yarn
RUN yarn run build

#### PRODUCTION
FROM marvambass/nginx-ssl-secure AS production
MAINTAINER isard <info@isard.com>

# Copy the frontend
COPY --from=build /app/dist /frontend

COPY dockers/nginx/nginx.conf /etc/nginx/
RUN mkdir /viewers
ADD ./src/webapp/static/viewers /viewers
RUN mkdir /errors
ADD dockers/nginx/errors/* /errors/
COPY dockers/nginx/dh.pem /
COPY dockers/nginx/auto-generate-certs.sh /opt
COPY dockers/nginx/entrypoint.sh /opt/
RUN chmod 744 /opt/*

FROM production AS development
