#!/bin/bash

mongo --host db-config-1 --port 27018 < /scripts/init-config.js
mongo --host db-shard-1a --port 27018 < /scripts/init-shard-1.js
mongo --host db-shard-2a --port 27018 < /scripts/init-shard-2.js
mongo --host db-shard-3a --port 27018 < /scripts/init-shard-3.js

mongoimport --host mongodb --db development --collection songs --type json --file /songs.json --jsonArray
mongo --host db-router --port 27018 < /scripts/init-index.js
