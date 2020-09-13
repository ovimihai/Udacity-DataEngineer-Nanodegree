Meets Specifications
--------------------

Dear Student,

Thank you for the extremely extraordinary effort you have put into this project. I'm impressed!\
I must tell you that this is one of the most well-formatted projects I ever happen to review.\
We look forward to no less than this great submission for the coming projects.\
Good luck and happy learning.

Friendly Note:\
Stay safe and take care of yourself and all your beloved ones in the current circumstances :)

Table Creation
--------------

The script, `create_tables.py`, runs in the terminal without errors. The script successfully connects to the Sparkify database, drops any tables if they exist, and creates the tables.

Runs with no single issue, thanks a lot! :)

CREATE statements in `sql_queries.py` specify all columns for each of the five tables with the right data types and conditions.

You did exactly as requested by my fellow previous reviewer, thank you for implementing this functionality!

--

Just for future reference:\
Adding the NOT NULL constraint to literally everything is not recommended at all, you might end up with an empty database and lose many interesting data points, let me help you modify that as well.\
For a real PostgreSQL project, you will probably end up doing the following each time:\
Since there are some columns in the songplay_table that are used as primary keys in other tables, you need to specify the NOT NULL constrain in these columns.\
These columns from the sognplay_table point of view are called foreign keys, they are used to join the fact table (songplay_table) with the other dimension tables, hence it's the best practice to force them not to be NULL.\
Also any column in any table that also happens to be a PRIMARY KEY of another table would require you to add the NOT NULL constraint to it as the best practice suggests.

ADVANCED:\
You can even add the FOREIGN KEY constraint, kindly check [this](https://stackoverflow.com/questions/655446/what-exactly-is-a-foreign-key) StackOverFlow answer to learn more about Foreign Keys.

I hope this ends up being useful for you one day.

ETL
---

The script, `etl.py`, runs in the terminal without errors. The script connects to the Sparkify database, extracts and processes the `log_data` and `song_data`, and loads data into the five tables.

Since this is a subset of the much larger dataset, the solution dataset will only have 1 row with values for value containing ID for both `songid` and `artistid` in the fact table. Those are the only 2 values that the query in the `sql_queries.py` will return that are not-NONE. The rest of the rows will have NONE values for those two variables.

Great job, this runs with no single issue!\
Thank you :)

INSERT statements are correctly written for each table, and handle existing records where appropriate. `songs` and `artists` tables are used to retrieve the correct information for the `songplays` INSERT.

Great job here!\
I would just like to give you a hint about something very crucial to this database.\
It's regarding the `level` column. This column specifies the level of the user, paid or free. Since you might be a paid user in one month and then switch to a free user the next month. Sparkify needs to learn about that! For many reasons:

-   Advertisement customization.
-   Like the application, Anghami, they give some privileges to paid users over the free users.

Business wise, you must not DO NOTHING, you need to UPDATE this entry.

* * * * *

I really hope this was insightful to you :)

Code Quality
------------

The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.

I wouldn't have written any better README than this .. impressive! :)

Scripts have an intuitive, easy-to-follow structure with code separated into logical functions. Naming for variables and functions follows the PEP8 style guidelines.

-   Your project code is clean and for the most part follows the PEP8 style guidelines.

-   I can clearly see your code structured into logical functions. Your function names clearly specify what your code is going to do. Great effort here!