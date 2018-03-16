# Music Library MVP

## Introduction
This is a python application which interfaces with mongoDB to read and updates a collection in that database.

_Note: This project assumes virtualenv and docker is installed_

## Requirements:
- JSON API Driven backenend written in Python.
- Data is stored in MongoDB, sample data provided `songs.json`.
- Anticipating massive scale with the Database growing to millions of documents.
- This backend will support a popular application with millions of users including unexpected spikes in activity.

## API Routes:
- GET /songs
  - Returns a list of songs with some details on them
  - Add possibility to paginate songs.

- GET /songs/avg/difficulty
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.

- GET /songs/search
  - Takes in parameter a 'message' string to search.
  - Return a list of songs. The search should take into account song's artist and title. The search should be case insensitive.

- POST /songs/rating
  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings should be between 1 and 5.

- GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.


# Notes

# Future Work

