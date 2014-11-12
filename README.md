OpenGov-API
===========

API for POSTing a csv files and returning the aggregation and file contents in json format.

Running OGchallenge.py in the folder given starts the "server" on localhost:5000.  

The project uses flask in order to create the API.  Instead of using an actual database, I store all of the file input in memory (which I believe can lead to issues depending on the memory allotted).  For our purposes, this should be fine.

At this time (and due to time constraints), the only method available is a POST method.  In the future, I want to be able to create GET methods to grab lines of the csv or aggregations of specific data and PUT methods to update the csv lines (and thus the aggregations).

transformation.py includes helper functions that I used in order to prevent the code from becoming too messy.

Known issues:
1. The output JSON is in the incorrect order.  This is due to the built in function jsonify reading the dictionary in key order.

2. Columns with commas separating values WITHIN the column break the API since the data cannot be parsed correctly.  The issue should be easy to fix, but since I currently only have a Windows machine available, without modifying the csv files to have windows line endings, it is much more difficult to read the csv file correctly.
