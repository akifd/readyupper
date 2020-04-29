FROM node:14
WORKDIR /code/readyupper

COPY readyupper/package.json readyupper/package-lock.json ./
RUN npm install
COPY readyupper .
