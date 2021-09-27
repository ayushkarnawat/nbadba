## Dataset creation

These scripts are meant to provide a convient (barebones) dataset for the NBA
basketball season. They include some SQLite specific code which makes it easier
to insert into the database, but gives no flexibility in terms of database
service one might want to use.

UPDATE: Scripts no longer work as the endpoints the NBA provides are no longer
valid and/or constantly change.

### NBA Stats API

DISCLIAMER: See https://github.com/bttmly/nba for more details on how to
document the failins within NBA STATS API and how these scripts no longer work.
It might be worthwhile to mention that there are NBA stats API written in a
bunch of languages (node.js, etc.) and should be used instead.

While these scripts were working as of 2019, recent tests show that the are
breaking due to NBA changing how one can access its endpoints successfully. As
such, it is probably best to use an API to retrieve data successfully. You can
use this to insert the data into a database server.

As the NBA statistics endpoints constantly changes, we are unsure if these
endpoints works
