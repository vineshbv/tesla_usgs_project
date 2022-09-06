"""
:Author: Vinesh Balagurusamy
: Version 1 : 04-09-2022
:Modified:

 __NOTE: docstrings__ <br>
 All docstrings in this file follow numpy style. <br>
 For more information see the docs:
    <https://numpydoc.readthedocs.io/en/latest/example.html>
"""
# ############################################################################
#                              IMPORT MODULES
# ############################################################################
import pandas as pd
import numpy as np
import requests
import datetime
import pyodbc


# ############################################################################
#            Return datetime format
# ############################################################################
def date_format(long_string):
    """
    :functionality - it returns the date time format
    """

    timestamp = datetime.datetime.fromtimestamp(long_string / 1e3)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


# ############################################################################
#            Return api into json response
# ############################################################################
def get_total_records(url):
    """
    :functionality - it returns the count of the events
    """

    response = requests.get(url)
    response_json = response.json()
    return response_json


# ############################################################################
#            Return api data into dataframe
# ############################################################################
def get_api_data(total_records):
    """
    :functionality - it returns the api data for the provided year
    """

    # results will be appended to this list
    all_items = []

    for offset in range(1, total_records, 20000):
        url = (
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2017-01-01&endtime=2017-12-31&limit=20000&offset="
            + str(offset)
        )
        response_json = requests.get(url).json()
        all_items.append(response_json)

    df_1 = pd.DataFrame()

    for i in range(0, len(all_items)):
        df_all_items = pd.DataFrame.from_dict(
            pd.json_normalize(all_items[i]), orient="columns"
        )
        df_1 = df_1.append(df_all_items)

    features_list = df_1["features"].tolist()

    df_2 = pd.DataFrame()

    for i in range(0, len(features_list)):
        df_feat_list = pd.DataFrame.from_dict(
            pd.json_normalize(features_list[i]), orient="columns"
        )
        df_2 = df_2.append(df_feat_list)

    return df_2


total_records_api = "https://earthquake.usgs.gov/fdsnws/event/1/count?starttime=2017-01-01&endtime=2017-12-31"

# Extract the total events
total_records = get_total_records(total_records_api)

# api data
df = get_api_data(total_records)

# Columns transformation
df["properties.time"] = df["properties.time"].apply(date_format)
df["Hour"] = df["properties.time"].str[11:13]
df["properties.time"] = df["properties.time"].str[:10]
labels = ["{0} - {1}".format(i, i + 1) for i in range(0, 6, 1)]
df["Magnitude_Range"] = pd.cut(
    df["properties.mag"], range(0, 7, 1), right=False, labels=labels
)
df["Magnitude_Range"] = np.where(df["properties.mag"] < 0, "<0", df["Magnitude_Range"])
df["Magnitude_Range"] = np.where(df["properties.mag"] >= 6, ">6", df["Magnitude_Range"])

df.rename(
    columns={
        "id": "Event_ID",
        "properties.mag": "Magnitude",
        "properties.place": "Place",
        "properties.time": "Date",
        "properties.url": "Url",
        "properties.detail": "Detail_Url",
        "properties.tsunami": "Tsunami_Flag",
        "properties.magType": "Magnitude_Type",
        "properties.title": "Title",
        "properties.type": "Type",
    },
    inplace=True,
)

# select required columns
final_df = df[
    [
        "Event_ID",
        "Type",
        "Title",
        "Date",
        "Hour",
        "Magnitude",
        "Magnitude_Type",
        "Magnitude_Range",
    ]
]

columns = [
    "Event_ID",
    "Type",
    "Title",
    "Date",
    "Hour",
    "Magnitude",
    "Magnitude_Type",
    "Magnitude_Range",
]

df_data = final_df[columns]
df_data = df_data.fillna("")
records = df_data.values.tolist()

# Connect to SQL Server
driver = "{ODBC Driver 17 for SQL Server}"
server = "servername"
database = "databasename"

conn = pyodbc.connect(
    "DRIVER="
    + driver
    + ";SERVER="
    + server
    + ";DATABASE="
    + database
    + ";Authentication=ActiveDirectoryInteractive;UID=usernameid",
    autocommit=True,
)

sql_insert = """
        INSERT INTO Valuation.EventsOverview
        VALUES (?, ?, ?, ?, 
                ?, ?, ?, ?
                )
             """

try:
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany(sql_insert, records)
    print(f"{len(df_data)} rows inserted to the table")
    cursor.commit()
except Exception as e:
    cursor.rollback()
    print(str(e[1]))
finally:
    print("Task is complete")
    cursor.close()
    conn.close()
