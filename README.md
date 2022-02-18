## GoJek take home assignment

### Running the application

We require Docker (with resource limit set to at least 3 GB memory) and docker-compose to build and run the application.

After cloning the project, simply run the following commands in the project root (take-home).

Install dependencies, download the dataset and run the unit test suite

$ ./bin/setup

Run the application (on port 8080 - changing this requires manual modification)

$ ./bin/run

### Design documentation

#### Web framework and libraries

I'm using Flask, a micro web application framework for Python. For reading and crunching the dataset I'm using the PyArrow and Pandas libraries. The whole application (including dependencies) is packaged using Docker.

#### Average fare heatmap

I ran into build errors while trying to install the S2 library. So for this assignment, I decided to write my own function to bin the latitudes and longitudes into a heatmap. We create a bounding box using the maximum and minimum latitude and longitude in the dataset, and divide it into N*N equal sized cells, where N is the grid side length (in number of cells).

Cells are numbered from 0 to N*N-1 in row-wise fashion. E.g. for a 2 x 2 grid - 
| 0 | 1 |
| 2 | 3 |

#### Data processing and storage

For this assignment, I chose to load the data from the Parquet file and keep it in-memory in Pandas dataframes. This makes it easy to write efficient analytics functions. Since all APIs require fetching trips corresponding to a date, I also created dataframes corresponding to each date and stored them in a dictionary with the date as the key.

#### Note on future scalability

For much bigger datasets, assuming we are still restricted to a single machine, I would need store the data on disk. A possible solution would be to store it in a relational database like MySQL or PostGRESQL, and create an index on the date column for efficiently fetching trips by date. We could speed this up by having an in-memory cache.