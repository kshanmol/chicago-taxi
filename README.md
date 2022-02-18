# take-home
GoJek take home test

Web framework and libraries - 

I'm using Flask, a micro web application framework for Python. For reading and crunching the dataset I'm using the PyArrow and Pandas libraries. The whole application (including dependencies) is packaged using Docker.

Data processing and storage -

For this assignment, I chose to load the data from the Parquet file and keep it in-memory in Pandas dataframes. This makes it easy to write efficient analytics functions. Since all APIs require fetching trips corresponding to a date, I also created dataframes corresponding to each date and stored them in a dictionary with the date as the key.

Scalability -

For much bigger datasets, assuming we are still restricted to a single machine, I would need store the data on disk. A possible solution would be to store it in a relational database like MySQL or PostGRESQL, and create an index on the date column for efficiently fetching trips by date. We could speed this up by having an in-memory cache.