FROM mvertes/alpine-mongo

ARG CONFIG1
ARG CONFIG2
ARG CONFIG3

CMD mongos --port 27017 --configdb configserver/$CONFIG1:27017,$CONFIG2:27017,$CONFIG3:27017
