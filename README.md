# sqlalchemy-challenge

Data analysis was conducted on climate data, and tools such as SQL, Pandas and Matplotlib were used to analyse a dataset conatining climate data from weather stations in Hawaii.

First a connection was established to SQL ALchemy, after which a precipitation data analysis was conducted. The datetime.strptime function was first used to calculate the date 1 year prior to the latest date, and this was saved in the one_year_ago variable. The precipitation was queried over the 12 month period and this data was saved as a Pandas dataframe. It was finally plotted as a bar chart.

Nex the total number of stations were counted using SQL's func.count function. Simlarly, the most active station having the greatest number of observations were also identified. The func.min, func.max and func.avg funcitons were used to calculate the lowest, highest and average temperatures. Next the data was further queried using SQL and the strftime function to clean and list the last 12 months' observations of the most active station. This data was then converted to a Pandas dataframe and plotted into a histogram. 

Next Flask was used to design a FLask API based on the climate data. The FLask API was designed in the app.py file, where more details on the code can be found.

Running the app.py file in python, the homepage can be accessed at: http://127.0.0.1:5000
And separate routes were built for the following:

http://127.0.0.1:5000/api/v1.0/precipitation: 	Returns last 12 months of precipitation data in JSON format.
http://127.0.0.1:5000/api/v1.0/stations: Returns a list of weather stations.
http://127.0.0.1:5000/api/v1.0/tobs: Returns last 12 months of temperature observations for the most active station.
http://127.0.0.1:5000/api/v1.0/<start>: Returns min, avg, and max temperature from the start date onward.
http://127.0.0.1:5000/api/v1.0/<start>/<end>: Returns min, avg, and max temperature for a given date range.