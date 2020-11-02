import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS 'staging_events';"
staging_songs_table_drop = "DROP TABLE IF EXISTS 'staging_songs';"
songplay_table_drop = "DROP TABLE IF EXISTS 'songplays';"
user_table_drop = "DROP TABLE IF EXISTS 'users';"
song_table_drop = "DROP TABLE IF EXISTS 'songs';"
artist_table_drop = "DROP TABLE IF EXISTS 'artists';"
time_table_drop = "DROP TABLE IF EXISTS 'time';"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
    artist			VARCHAR	NOT NULL,
    auth			VARCHAR	NOT NULL,
    firstName		VARCHAR	NOT NULL,
    gender			VARCHAR	NOT NULL,
    itemSession		INTEGER	NOT NULL,
    lastName		VARCHAR	NOT NULL,
    length			FLOAT	NOT NULL,
    level			VARCHAR	NOT NULL,
    location		VARCHAR	NOT NULL,
    method			VARCHAR	NOT NULL,
    page			TEXT	NOT NULL,
    registration	FLOAT	NOT NULL,
    sessionId		INTEGER	NOT NULL,
    song			VARCHAR	NOT NULL,
    status			INTEGER	NOT NULL,
    ts				TIMESTAMP	NOT NULL,
    userAgent		VARCHAR	NOT NULL,
    userId			INTEGER	NOT NULL
)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    num_songs			INTEGER	NOT NULL,
    artist_id			VARCHAR	NOT NULL,
    artist_latitude		DECIMAL(10,5)	NOT NULL,
    artist_longitude	DECIMAL(10,5)	NOT NULL,
    artist_location		VARCHAR	NOT NULL,
    artist_name			VARCHAR	NOT NULL,
    song_id				VARCHAR	NOT NULL,
    title				VARCHAR	NOT NULL,
    duration			FLOAT	NOT NULL,
    year				INTEGER	NOT NULL
)
""")

songplay_table_create = ("""
""")

user_table_create = ("""
""")

song_table_create = ("""
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
