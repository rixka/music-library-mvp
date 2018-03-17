FROM mvertes/alpine-mongo

RUN apk add --no-cache mongodb-tools

COPY songs.json /songs.json
ADD scripts /scripts

CMD sh /scripts/init.sh
