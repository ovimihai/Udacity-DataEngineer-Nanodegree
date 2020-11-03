import configparser
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

DWH_DB                 = config.get("CLUSTER","DB_NAME")
DWH_DB_USER            = config.get("CLUSTER","DB_USER")
DWH_DB_PASSWORD        = config.get("CLUSTER","DB_PASSWORD")
DWH_PORT               = config.get("CLUSTER","DB_PORT")
DWH_ENDPOINT           = config.get("CLUSTER","HOST")

import psycopg2
con=psycopg2.connect(dbname= DWH_DB, host=DWH_ENDPOINT, port= DWH_PORT, user=DWH_DB_USER, password=DWH_DB_PASSWORD)


# Verify data
table_counts = {
    'staging_events':8056, 
    'staging_songs':14896,
    'songplays':333,
    'users':104,
    'songs':14896,
    'artists':10025,
    'time':333
}

for table, count in table_counts.items():
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM {};".format(table))
    r = cur.fetchone()
    assert r[0] == count, "Invalid count for table {}".format(table)
    cur.close()

print("Done")