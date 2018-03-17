FROM mvertes/alpine-mongo

RUN mkdir -p /data/configdb
CMD mongod --port 27017 --configsvr --replSet configserver --noprealloc --smallfiles --oplogSize 16
