FROM mvertes/alpine-mongo

RUN apk add --no-cache mongodb-tools

COPY songs.json /songs.json
COPY init.sh /init.sh
COPY init.js /init.js
#CMD mongoimport --host mongodb --db development --collection songs --type json --file /songs.json --jsonArray
CMD sh /init.sh
