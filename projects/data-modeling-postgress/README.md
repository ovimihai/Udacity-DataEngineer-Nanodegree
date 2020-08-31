# Sparkify Song Play Analysis
by Ovidiu Anicai

Sparkify is a startup that wants to analyze the data they collected from their new music streaming app. They want to find out what songs are their user listening to.
Because they have the data in multiple folders in JSON files, I, as a data engineer, I have to create a Postgress database enable the company to make the desired queries.

I have to model the data so we can do the desired analysist and build a ETL pipeline to load the data into Postgress.

The schema design follows the Star Schema pattern and it has in the middle the Facts Table called `songplays`. All around this table we have the different Dimensions Tables like `users`, `songs`, `artists` and `time`

![Schema](schema.png "https://dbdiagram.io/d/5f4d514188d052352cb578bb")

## Queries

As we have a small sample of a bigger database, song_id and artist_id match only once. The interesting query would be what is the most listened of them all

```
SELECT song_id, COUNT(*) as listened_no 
FROM songplays 
GROUP BY song_id 
ORDER BY listened_no DESC 
LIMIT 10;
```

But since we can't do that, we can still get the busiesty Location from our database:

```
SELECT location, COUNT(*) as count 
FROM songplays 
GROUP BY location 
ORDER BY count DESC
LIMIT 10;
```
And the results are:

| Location                                | Count |
|-----------------------------------------|-------|
| San Francisco-Oakland-Hayward, CA       |   784 |
| Portland-South Portland, ME             |   701 |
| Lansing-East Lansing, MI                |   557 |
| Atlanta-Sandy Springs-Roswell, GA       |   496 |
| Chicago-Naperville-Elgin, IL-IN-WI      |   475 |
| Waterloo-Cedar Falls, IA                |   401 |
| Lake Havasu City-Kingman, AZ            |   350 |
| Tampa-St. Petersburg-Clearwater, FL     |   311 |
| San Jose-Sunnyvale-Santa Clara, CA      |   299 |
| Birmingham-Hoover, AL                   |   292 |