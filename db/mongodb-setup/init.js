use development;
db.createCollection('ratings')
db.songs.createIndex({ title: 'text', artist: 'text' });
