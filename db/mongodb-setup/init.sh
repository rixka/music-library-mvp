#!/bin/bash

mongoimport --host mongodb --db development --collection songs --type json --file /songs.json --jsonArray
mongo --host mongodb < init.js
