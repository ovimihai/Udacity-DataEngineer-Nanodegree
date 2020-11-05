Requires Changes
----------------

### 4 specifications require changes

Almost there!!! ![:clap:](https://review.udacity.com/assets/images/emojis/clap.png ":clap:")

Good work student, your project looks promising but it still needs some extra work from you, go for it!!!![:muscle:](https://review.udacity.com/assets/images/emojis/muscle.png ":muscle:")

All the best,\
![:udacious:](https://review.udacity.com/assets/images/emojis/udacious.png ":udacious:")

Table Creation
--------------

The script, create_tables.py, runs in the terminal without errors. The script successfully connects to the Sparkify database, drops any tables if they exist, and creates the tables.

CREATE statements in sql_queries.py specify all columns for both the songs and logs staging tables with the right data types and conditions.

Staging tables look almost ok, there is just a small issue with the 'ts' column, which should be defined as TIMESTAMP. Kindly check it.

CREATE statements in sql_queries.py specify all columns for each of the five tables with the right data types and conditions.

Kindly review all fact/dimension tables definitions keeping in mind these four rules:

-   All tables must have a PRIMARY KEY
-   All columns which reference foreign primary keys, must be defined with NOT NULL option enabled
-   All other columns should allow NULL values.
-   No DISTKEY/SORTKEY is needed

ETL
---

The script, `etl.py`, runs in the terminal without errors. The script connects to the Sparkify redshift database, loads `log_data` and `song_data` into staging tables, and transforms them into the five tables.

Let's check this point after fixing previous issues

INSERT statements are correctly written for each table and handles duplicate records where appropriate. Both staging tables are used to insert data into the songplays table.

The INSERT statements look ok, you did include SELECT DISTINCT to avoid duplicated data, and you did also include NextSong filter. But you might need to add some extra conditions after fixing the fact/dimension tables definitions.

Code Quality
------------

The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.

Your README looks ![:ok:](https://review.udacity.com/assets/images/emojis/ok.png ":ok:") to me

Scripts have an intuitive, easy-to-follow structure with code separated into logical functions. Naming for variables and functions follows the PEP8 style guidelines.

Kindly include pep8 style docstrings in all Python functions, this is an example:

[![Screenshot_20180421_100226.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/127682/1604473698/Screenshot_20180421_100226.png)](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/127682/1604473698/Screenshot_20180421_100226.png)
