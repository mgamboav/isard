# Build stage
FROM node:lts-alpine as build-stage

COPY ./src/new_webapp/frontend /app

WORKDIR /app
RUN yarn
RUN yarn run build

# Production stage
FROM marvambass/nginx-ssl-secure as production-stage
MAINTAINER isard <info@isard.com>

# Copy the frontend
COPY --from=build-stage /app/dist /frontend

COPY dockers/nginx/nginx.conf /etc/nginx/
RUN mkdir /viewers
ADD ./src/webapp/static/viewers /viewers
RUN mkdir /errors
ADD dockers/nginx/errors/* /errors/
COPY dockers/nginx/dh.pem /
COPY dockers/nginx/auto-generate-certs.sh /opt
COPY dockers/nginx/entrypoint.sh /opt/
RUN chmod 744 /opt/*
