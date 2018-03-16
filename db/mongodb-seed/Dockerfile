FROM mvertes/alpine-mongo

RUN apk add --no-cache mongodb-tools

COPY songs.json /songs.json
CMD mongoimport --host mongodb --db development --collection songs --type json --file /songs.json --jsonArray
