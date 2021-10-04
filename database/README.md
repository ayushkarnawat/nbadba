## Basketball Statistics Database

We provide a basic API to query specific endpoints provided by the NBA to
retrieve data about teams, players, coaches, teams, and games (from any season).

We purposefully design the API to be decoupled from the specific Database
Management System (DBMS) insertion code. This provides flexibility in terms of
which different services (e.g. SQLite, Postgres, MySQL) can be used with the
app.


### SQLite Creation

We provide a basic script to retrieve and insert information into our database.
For local developmental purposes, we provide a small footprint (barebones)
database that contains some (basic) information to populate inside the app.

To add more information (e.g. other season information), you can modify the
`create_db.py` file to insert the specific data you want. Note: These scripts
are just meant to provide a canonical db which fits our database design.

UPDATE: Scripts no longer work as the endpoints the NBA provides are no longer
valid and/or constantly change.


### Important notes

It appears as the NBA has been blacklisted IP addresses, e.g. those providede by
cloud services, but also many local ones too. As such, these GET requests no
longer work, and, annonying, just seem to hang. As such, do not be surprised if
this no longer work on any machine.

While these scripts were working as of 2019, recent tests show that the are
breaking (due to reasons above). Better maintained packages, with better
designed APIs (with support for many languages such as node.js, python, etc.)
should be used instead.
