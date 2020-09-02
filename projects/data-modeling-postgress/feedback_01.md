Requires Changes
----------------

### 4 specifications require changes

You've made a great effort in your work in the project! Your submission is almost there in terms of meeting specifications, but there are a few issues that need to be revised before the project can pass all rubric points. See below for some suggestions on revisions that can be made for your next project submission! In case you have any queries please use the knowledge board or leave questions in student notes, we are happy to help!

Good Luck in your next submission![:smile:](https://review.udacity.com/assets/images/emojis/smile.png ":smile:")

Table Creation
--------------

The script, `create_tables.py`, runs in the terminal without errors. The script successfully connects to the Sparkify database, drops any tables if they exist, and creates the tables.

Nicely done! Your create_tables.py drops the tables if they exist, and creates them properly!

CREATE statements in `sql_queries.py` specify all columns for each of the five tables with the right data types and conditions.

Good first attempt! You have created dimension and fact tables as required in the template. However, the dimensions tables currently do not specify which primary key should exist for each table and does not specify NOT NULLs. Please revise your sql_queries.py with that info. This website can provide additional information if you need further help understanding which column should become your primary key and which columns should not be NULL.\
<https://www.postgresql.org/docs/9.4/ddl-constraints.html>

ETL
---

The script, `etl.py`, runs in the terminal without errors. The script connects to the Sparkify database, extracts and processes the `log_data` and `song_data`, and loads data into the five tables.

Since this is a subset of the much larger dataset, the solution dataset will only have 1 row with values for value containing ID for both `songid` and `artistid` in the fact table. Those are the only 2 values that the query in the `sql_queries.py` will return that are not-NONE. The rest of the rows will have NONE values for those two variables.

This will be reviewed once you made above changes.

INSERT statements are correctly written for each table, and handle existing records where appropriate. `songs` and `artists` tables are used to retrieve the correct information for the `songplays` INSERT.

Good first attempt! Next, think about what happens when there is a CONFLICT. For e.g., in user_table_insert, what if there is a CONFLICT on user_id, how do you want the table to handle that? Should it UPDATE the level? Again, check this link to think about that: <https://www.postgresql.org/docs/9.5/sql-insert.html>

Code Quality
------------

The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.

-   Very good job here! However, I will suggest you elaborate more on your ETL pipeline.
-   It would be nice to see an example of how the duplication occurred (maybe just referencing the variable/column name) and which tables?
-   Check this link to get an idea of how to write a good README: <https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project>

Scripts have an intuitive, easy-to-follow structure with code separated into logical functions. Naming for variables and functions follows the PEP8 style guidelines.

-   Add [docstrings](https://www.geeksforgeeks.org/python-docstrings/) for all the functions.
-   Make sql_queries more readable by writing them in multiple lines.
-   Check [this link](https://stackoverflow.com/questions/32750833/how-to-format-long-sql-queries-according-to-pep8) to read about how to format long sql queries.