# tesla_usgs_project
Tesla Coding Challenge

# Author: Vinesh
# Date : 04-09-2022

**Objective**:
1) Please query all events that have occurred during year 2017
2) Read a JSON response from the API
3) Design the database objects required to store the result in a relational fashion.
4) Store the response in those objects
5) Provide query/analysis to give biggest earthquake of 2017
6) Provide query/analysis to give most probable hour of the day for the earthquakes bucketed by the range of magnitude (0-1,1-2,2-3,3-4,4-5,5-6,>6   For border values in the bucket, include them in the bucket where the value is a lower limit so for 1 include it in 1-2 bucket)

**Deliverables**:
1) usgs_main.py - This script reads the api data for the year 2017 and stores the dataframe into the SQL table Valuation.EventsOverview
2) DB Schema.sql - Table Valuation.EventsOverview schema
3) TotalEvents.png - Displays the Total events occurred during year 2017 with the raw data
4) BiggestEarthQuake_Analysis.png - Depicts the biggest earth quake of the year 2017 (highlighted in red)
5) MostProbableHour.png - Matrix visualization of the probable hour of the day for the earthquakes bucketed by the range of magnitude 
6) Queries.sql - Queries for item 1, 5 & 6 in objective section
