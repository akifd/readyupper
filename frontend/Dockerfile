FROM node:14
WORKDIR /code/readyupper

COPY readyupper/package.json .
RUN npm install
COPY readyupper .

CMD ["npm", "start"]
