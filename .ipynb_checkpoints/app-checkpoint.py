{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.dates as mdates\n",
    "from matplotlib.dates import (DAILY, rrulewrapper, RRuleLocator)\n",
    "import math"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import datetime as dt\n",
    "from datetime import timedelta"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Reflect Tables into SQLAlchemy ORM"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Python SQL toolkit and Object Relational Mapper\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func, inspect"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['measurement', 'station']"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# We can view all of the classes that automap found\n",
    "Base.classes.keys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create our session (link) from Python to the DB\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Exploratory Climate Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "id INTEGER\n",
      "station TEXT\n",
      "date TEXT\n",
      "prcp FLOAT\n",
      "tobs FLOAT\n"
     ]
    }
   ],
   "source": [
    "inspector = inspect(engine)\n",
    "inspector.get_table_names()\n",
    "columns = inspector.get_columns('Measurement')\n",
    "for column in columns:\n",
    "    print(column[\"name\"], column[\"type\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "('2017-08-23')"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "results = session.query(func.Max(Measurement.date))\n",
    "[maxdate] = [result for result in results]\n",
    "maxdate"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Date</th>\n",
       "      <th>prcp</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2016-08-24</td>\n",
       "      <td>1.555000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2016-08-25</td>\n",
       "      <td>0.077143</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2016-08-26</td>\n",
       "      <td>0.016667</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>2016-08-27</td>\n",
       "      <td>0.064000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2016-08-28</td>\n",
       "      <td>0.516667</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>360</th>\n",
       "      <td>2017-08-19</td>\n",
       "      <td>0.030000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>361</th>\n",
       "      <td>2017-08-20</td>\n",
       "      <td>0.005000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>362</th>\n",
       "      <td>2017-08-21</td>\n",
       "      <td>0.193333</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>363</th>\n",
       "      <td>2017-08-22</td>\n",
       "      <td>0.166667</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>364</th>\n",
       "      <td>2017-08-23</td>\n",
       "      <td>0.132500</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>365 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "          Date      prcp\n",
       "0   2016-08-24  1.555000\n",
       "1   2016-08-25  0.077143\n",
       "2   2016-08-26  0.016667\n",
       "3   2016-08-27  0.064000\n",
       "4   2016-08-28  0.516667\n",
       "..         ...       ...\n",
       "360 2017-08-19  0.030000\n",
       "361 2017-08-20  0.005000\n",
       "362 2017-08-21  0.193333\n",
       "363 2017-08-22  0.166667\n",
       "364 2017-08-23  0.132500\n",
       "\n",
       "[365 rows x 2 columns]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Set begindate the date 1 year ago from the last data point in the database\n",
    "begindate = dt.datetime(2016, 8, 23)\n",
    "\n",
    "# Perform a query to retrieve the data and precipitation scores\n",
    "lastyeardata = session.query(Measurement.date, func.Avg(Measurement.prcp)).\\\n",
    "    filter(Measurement.date >= begindate).\\\n",
    "    group_by(Measurement.date).\\\n",
    "    order_by(Measurement.date).all()\n",
    "\n",
    "# Save the query results as a Pandas DataFrame sorted by date\n",
    "Prcpdf = pd.DataFrame(lastyeardata, columns=['Date', 'prcp'])\n",
    "\n",
    "\n",
    "#convert string date types to date\n",
    "Prcpdf['Date'] = pd.to_datetime(Prcpdf['Date'], format='%Y-%m-%d')\n",
    "Prcpdf"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "#define for setting xticks\n",
    "rule = rrulewrapper(DAILY, interval=25)\n",
    "loc = RRuleLocator(rule)\n",
    "\n",
    "#set plot figure size\n",
    "plt.figure(figsize=(15,5))\n",
    "\n",
    "#plot chart and set/format xticks\n",
    "plt.bar(Prcpdf['Date'], Prcpdf['prcp'], color='b', align=\"center\")\n",
    "plt.gca().xaxis.set_major_locator(loc)\n",
    "plt.xticks(rotation=75)\n",
    "\n",
    "#set labels\n",
    "plt.title(\"Precipitation in the last year\")\n",
    "plt.ylabel(\"Inches\")\n",
    "plt.xlabel(\"Date\")\n",
    "\n",
    "#set axes limits\n",
    "plt.xlim(dt.datetime(2016, 8, 20),  dt.datetime(2017, 8, 25))\n",
    "\n",
    "\n",
    "#chart properties\n",
    "plt.grid(True)\n",
    "#plt.tight_layout()\n",
    "\n",
    "#show chart\n",
    "plt.show()\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "count    365.000000\n",
       "mean       0.169987\n",
       "std        0.295722\n",
       "min        0.000000\n",
       "25%        0.008571\n",
       "50%        0.070000\n",
       "75%        0.191667\n",
       "max        2.380000\n",
       "Name: prcp, dtype: float64"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use Pandas to calcualte the summary statistics for the precipitation data\n",
    "Prcpdf['prcp'].describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "9\n"
     ]
    }
   ],
   "source": [
    "# Design a query to show how many stations are available in this dataset?\n",
    "stations = session.query(Measurement.station).group_by(Measurement.station).all()\n",
    "print(len(stations))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "('USC00519281', 2772)"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# What are the most active stations? (i.e. what stations have the most rows)?\n",
    "mostactivestation = session.query(Measurement.station, func.count(Measurement.id)).\\\n",
    "                        group_by(Measurement.station).\\\n",
    "                        order_by(func.count(Measurement.id).desc()).first()\n",
    "\n",
    "mostactivestation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " Lowest Temp recoreded for station USC00519281 is 54.0\n",
      " Highest Temp recoreded for station USC00519281 is 85.0\n",
      " Average Temp recoreded for station USC00519281 is 71.66\n"
     ]
    }
   ],
   "source": [
    "# Using the station id from the previous query, calculate the lowest temperature recorded, \n",
    "# highest temperature recorded, and average temperature of the most active station?\n",
    "activestats = session.query(func.Min(Measurement.tobs), func.Max(Measurement.tobs), func.Avg(Measurement.tobs)).\\\n",
    "                        filter(Measurement.station=='USC00519281').\\\n",
    "                        group_by(Measurement.station).all()\n",
    "activestats\n",
    "[stats] = [result for result in activestats]\n",
    "print(f\" Lowest Temp recoreded for station USC00519281 is {stats[0]}\")\n",
    "print(f\" Highest Temp recoreded for station USC00519281 is {stats[1]}\")\n",
    "print(f\" Average Temp recoreded for station USC00519281 is {round(stats[2],2)}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[('USC00519281', 2772),\n",
       " ('USC00519397', 2724),\n",
       " ('USC00513117', 2709),\n",
       " ('USC00519523', 2669),\n",
       " ('USC00516128', 2612),\n",
       " ('USC00514830', 2202),\n",
       " ('USC00511918', 1979),\n",
       " ('USC00517948', 1372),\n",
       " ('USC00518838', 511)]"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Choose the station with the highest number of temperature observations.\n",
    "\n",
    "lastyeartobs = session.query(Measurement.station, func.Count(Measurement.tobs)).\\\n",
    "                    group_by(Measurement.station).\\\n",
    "                    order_by(func.Count(Measurement.station).desc()).all()\n",
    "                             \n",
    "lastyeartobs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>tobs</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>54.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>56.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>56.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>56.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>56.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2767</th>\n",
       "      <td>83.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2768</th>\n",
       "      <td>83.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2769</th>\n",
       "      <td>83.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2770</th>\n",
       "      <td>84.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2771</th>\n",
       "      <td>85.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2772 rows × 1 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "      tobs\n",
       "0     54.0\n",
       "1     56.0\n",
       "2     56.0\n",
       "3     56.0\n",
       "4     56.0\n",
       "...    ...\n",
       "2767  83.0\n",
       "2768  83.0\n",
       "2769  83.0\n",
       "2770  84.0\n",
       "2771  85.0\n",
       "\n",
       "[2772 rows x 1 columns]"
      ]
     },
     "execution_count": 74,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Query the last 12 months of temperature observation data for this station and plot the results as a histogram\n",
    "tobs = session.query(Measurement.tobs).\\\n",
    "                    filter(Measurement.station=='USC00519281').\\\n",
    "                    order_by(Measurement.tobs).all()\n",
    "\n",
    "\n",
    "# creare dataframe for results\n",
    "tobsdf = pd.DataFrame(tobs)\n",
    "tobsdf\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAYUAAAEWCAYAAACJ0YulAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nO3df5xcdX3v8dfbhB+BhSQIbmOCBiRyJUSpWVC01d2GCv4M9iEaL2rworG38QeaWoP2UWPbVHoVtRXRpkCNRlliCpcoRYTURW2FQBQNAZEIMSTBjcQEXMwNbvzcP853jyezM7uTzZ6dnd338/GYx5zzPd9zzuc7Z2Y+c37M9ygiMDMzA3haowMwM7PRw0nBzMxyTgpmZpZzUjAzs5yTgpmZ5ZwUzMws56RgZmY5J4UmJamn8PidpL2F8QsbHd9QSNoi6ZwRXN8ySSHpvRXll6TyZSMVSzNJr9uqOur9T0l3p/fko5JulvRHIxBfSDql7PWMVU4KTSoiWvoewFbgtYWyrzQ6vkqSJo7SdfwUWFhR9rZUPmqMxOs3nCR9APgM8A9AK/As4EpgfiPjssE5KYwxkp4maamkn0naJWm1pOPStJnpV9TbJT0iabekP5d0pqQfS9oj6YrCsi6S9F+SPivpcUk/kTSvMH2ypKvTr8Dtkv5e0oSKeT8t6VfAMknPkfSfKa7HJH1F0pRU/8tkXxxfT78s/0pSu6RtFe3L9ybSL9Y1klZJegK4aKCYargLOErS7LTM2cCkVF5c72sk3ZNeo/+W9PzCtL7X+9eS7pP0+sK0UyTdnl6/xyRdV7EtJhbqdkl6xwCv3xGSPilpq6RuSV+QNCnVb5e0Lb1uO1P7z5f0Kkk/lfQrSR8+yPfJwrSuxyR9JE07D/gw8Ka0nX5U5T04GfhbYHFEXB8RT0bEbyPi6xHxwVTnCEmfkbQjPT4j6YhC279Xscz817+kL0r6nKSb0mt+p6TnpGnfSbP8KMX3JknHS/pG2na/kvRdSf7uq8EvzNjzXuB84OXAM4HdwOcq6rwImAW8iezX3EeAc4DZwBslvbyi7kPA8cBHgev7vjyAlUAvcArwh8ArgHdUmfcZwHJAwMdTXM8DTgSWAUTEWzlwj+f/1Nne+cAaYArwlTpiqubLZHsHkO01fKk4UdILgWuAdwFPB/4FWNv3JQb8DPhjYDLwMWCVpGlp2t8B3wKmAjOAz9bZLuj/+v0j8FzgjNS+6cDfFOr/AXBkofxfgbcAc1N8fyPp5FS3nvfJHwGnAvPSvM+LiG+S/fq/Lm2nF1SJ++wUxw0DtO0jwItTW14AnAX89QD1K72Z7LWeCmwme32IiJel6S9I8V0HLAG2ASeQ7bV8GHD/PrVEhB9N/gC2AOek4fuBeYVp04DfAhOBmWQfhumF6buANxXG/x24JA1fBOwAVJi+Hngr2YdrHzCpMO3NwLcL824dJO7zgR9Wa0cabwe2DdDWZcB3CtMGjKnK+pcBq8j2ULYCh6XnE1P5slTv88DfVcz7APDyGsu9B5ifhr8ErABmVNTp2xYTC2VdwDuqvX5kCfVJ4DmFsrOBhwuv1V5gQho/Ji3/RYX6G4DzD+J9MqMwfT2woPi6DbBdLwR+Mci2/xnwqsL4ucCWQtu/V1E/gFPS8BeBqwrTXgX8pFrdNP63wI3FMj9qP5rqOKXV5dnADZJ+VyjbT/aF2ae7MLy3ynhLYXx7pE9W8nOyX5bPJvsSfVRS37SnAY8U6haHkfQM4J/JfrUek+rvrqtVtRXXUU9M/UTEVkmbyX4BPxgRjxTm71vuQknvKZQdTvY6IOltwAfIvkwhe/2OT8N/Rba3sF7SbuDyiLhmCG07ATgK2FCITUDx0NiuiNifhvem51rbtp73yS8Kw7/hwPfFQHYBx0uaGBG9Neo8k+y91KfvfVWvg4ntE2SJ7FvptVsREZcdxLrGFR8+GnseAV4ZEVMKjyMjYvsQlzddB35DPots7+ERsl/lxxfWc2xEzC7UrdxF/3gqe35EHEt2aEMD1H+S7IsQgHRu4ISKOsV56ompli+RHWb4UpVpjwDLK17ToyLiWknPJjtM827g6RExBbi3r10R8YuIeGdEPJPs8NOV6dj4k2nZRxXW8wcDtO0xsi/12YUYJkd2ocFQHMr7ZLBDL98H/h/ZnmAtO8gSU5++9xX03+6Vr8tBiYhfR8SSiDgZeC3wARXOjdmBnBTGni8Ay9OXFZJOkHQoV3w8A3ivpMMkXUB2LuA/IuJRsmPll0s6Np24fE7F+YhKxwA9wB5J04EPVkzvBk4ujP8UOFLSqyUdRnbM+QhqGGJMfa4jO/+wusq0fwX+XNKLlDk6xXQMcDTZl+QvASS9HTi9b0ZJF0iakUZ3p7r7I+KXwHbgLZImSPpfwHMGaNvvUhyfTntcSJou6dw62lbNobxPuoGZtU7WRsTjZOc0PpdOdh+V3j+vlNR3ruha4K/Teo9P9fsuc/0RMFvSGZKOJJ13OggHvI+UXSRwSvpx8wTZHtH+WjOPd04KY88/AWvJdpV/DdxBdsJyqO4kOyn9GNnJvDdExK407W1kh1HuI/vCW0N2bLqWjwEvBB4HbgKur5j+cbIvij2S/jJ9ufwFcBXZF+iTZCcMB3KwMQEQEXsj4raI2Ftl2t3AO4Er0jI3kx33JiLuAy4n+3XcDcwB/qsw+5nAnZJ6yLbL+yLi4TTtnWSJcRfZSf7/HiTMD6V136HsaqvbyE4ED8WhvE++lp53SfpBtQoR8SmyQ2p/TZYwHyHbm/q/qcrfA3cDPwY2Aj9IZUTET8nOA9wGPAgccCVSHZYBK9P76I1k79/byH6QfB+4MiK6DnKZ44YOPFxs9nuSLiI78Vn6H47MbHTwnoKZmeWcFMzMLOfDR2ZmlvOegpmZ5Zr6z2vHH398zJw5s9R1PPnkkxx99NGlrqNsY6ENMDba4TaMDuO9DRs2bHgsIir/8wM0eVKYOXMmd999d6nr6Orqor29vdR1lG0stAHGRjvchtFhvLdB0s9rTfPhIzMzy5WaFCS9X9ImSfdKulbSkZKOk3SrpAfT89RC/UslbZb0wCH8U9PMzIaotKSQujF4L9AWEaeTddy1AFgKrIuIWcC6NI6k09L02cB5ZH3EDNQPvpmZDbOyDx9NBCYpu5HIUWQdXs0n6/Oe9NzXadZ8oDMi9qVuADaT9bFuZmYjpNT/KUh6H1l/OXuBb0XEhZL2pJ4k++rsjoipyu74dUdErErlVwM3R8SaimUuAhYBtLa2zu3s7CwtfoCenh5aWobaEeXoMBbaAGOjHW7D6DDe29DR0bEhItqqTSvt6qN0rmA+cBKwB/iapLcMNEuVsn4ZKyJWkN20hLa2tij7CoLxfpXCaDIW2uE2jA5uQ21lHj46h+yuUL+MiN+S9Yj5EqC771aF6Xlnqr+N7I5XfWbw+/7VzcxsBJSZFLYCL059qYvsPq/3k3XXuzDVWUh2mzxS+QJlN/Q+iay72/UlxmdmZhVKO3wUEXdKWkPWT3ov8EOywz4twGpJF5MljgtS/U2SVpP1g98LLC7cWtDMzEZAqf9ojoiPAh+tKN5HttdQrf5yshPTZk1v5tKb+pUtmdPLRVXKh2rLZa8etmWZgf/RbGZmBU4KZmaWc1IwM7Ock4KZmeWcFMzMLOekYGZmOScFMzPLOSmYmVnOScHMzHJOCmZmlnNSMDOznJOCmZnlnBTMzCznpGBmZjknBTMzyzkpmJlZzknBzMxypSUFSadKuqfweELSJZKOk3SrpAfT89TCPJdK2izpAUnnlhWbmZlVV1pSiIgHIuKMiDgDmAv8BrgBWAqsi4hZwLo0jqTTgAXAbOA84EpJE8qKz8zM+hupw0fzgJ9FxM+B+cDKVL4SOD8Nzwc6I2JfRDwMbAbOGqH4zMwMUESUvxLpGuAHEXGFpD0RMaUwbXdETJV0BXBHRKxK5VcDN0fEmoplLQIWAbS2ts7t7OwsNfaenh5aWlpKXUfZxkIboPnasXH74/3KWidB997hW8ec6ZOHb2F1arbtUM14b0NHR8eGiGirNm3iIUVVB0mHA68DLh2sapWyfhkrIlYAKwDa2tqivb39UEMcUFdXF2Wvo2xjoQ3QfO24aOlN/cqWzOnl8o3D97HbcmH7sC2rXs22HapxG2obicNHryTbS+hO492SpgGk552pfBtwYmG+GcCOEYjPzMySkUgKbwauLYyvBRam4YXAjYXyBZKOkHQSMAtYPwLxmZlZUurhI0lHAX8KvKtQfBmwWtLFwFbgAoCI2CRpNXAf0Assjoj9ZcZnZmYHKjUpRMRvgKdXlO0iuxqpWv3lwPIyYzIzs9r8j2YzM8s5KZiZWc5JwczMck4KZmaWc1IwM7Ock4KZmeWcFMzMLOekYGZmOScFMzPLOSmYmVnOScHMzHJOCmZmlnNSMDOznJOCmZnlnBTMzCznpGBmZjknBTMzyzkpmJlZrtSkIGmKpDWSfiLpfklnSzpO0q2SHkzPUwv1L5W0WdIDks4tMzYzM+uv7D2FfwK+GRH/A3gBcD+wFFgXEbOAdWkcSacBC4DZwHnAlZImlByfmZkVlJYUJB0LvAy4GiAinoqIPcB8YGWqthI4Pw3PBzojYl9EPAxsBs4qKz4zM+tPEVHOgqUzgBXAfWR7CRuA9wHbI2JKod7uiJgq6QrgjohYlcqvBm6OiDUVy10ELAJobW2d29nZWUr8fXp6emhpaSl1HWUbC22A5mvHxu2P9ytrnQTde4dvHXOmTx6+hdWp2bZDNeO9DR0dHRsioq3atImHFNXAJgIvBN4TEXdK+ifSoaIaVKWsX8aKiBVkyYa2trZob28fhlBr6+rqoux1lG0stAGarx0XLb2pX9mSOb1cvnH4PnZbLmwftmXVq9m2QzVuQ21lnlPYBmyLiDvT+BqyJNEtaRpAet5ZqH9iYf4ZwI4S4zMzswqlJYWI+AXwiKRTU9E8skNJa4GFqWwhcGMaXgsskHSEpJOAWcD6suIzM7P+yjx8BPAe4CuSDgceAt5OlohWS7oY2ApcABARmyStJkscvcDiiNhfcnxmZlZQalKIiHuAaicz5tWovxxYXmZMZmZWm//RbGZmOScFMzPLOSmYmVnOScHMzHJOCmZmlnNSMDOznJOCmZnlnBTMzCznpGBmZjknBTMzy5Xd95GZlWhmle65h9uWy15d+jps9PCegpmZ5ZwUzMws56RgZmY5JwUzM8s5KZiZWc5JwczMcqUmBUlbJG2UdI+ku1PZcZJulfRgep5aqH+ppM2SHpB0bpmxmZlZfyOxp9AREWdERN9tOZcC6yJiFrAujSPpNGABMBs4D7hS0oQRiM/MzJJGHD6aD6xMwyuB8wvlnRGxLyIeBjYDZzUgPjOzcUsRUd7CpYeB3UAA/xIRKyTtiYgphTq7I2KqpCuAOyJiVSq/Grg5ItZULHMRsAigtbV1bmdnZ2nxA/T09NDS0lLqOso2FtoAzdeOjdsf71fWOgm69zYgmEMwZ/rkA8abbTtUM97b0NHRsaFw9OYAZXdz8dKI2CHpGcCtkn4yQF1VKeuXsSJiBbACoK2tLdrb24cl0Fq6urooex1lGwttgOZrx0VVuqBYMqeXyzc2V+8yWy5sP2C82bZDNW5DbaUePoqIHel5J3AD2eGgbknTANLzzlR9G3BiYfYZwI4y4zMzswOVlhQkHS3pmL5h4BXAvcBaYGGqthC4MQ2vBRZIOkLSScAsYH1Z8ZmZWX9l7se2AjdI6lvPVyPim5LuAlZLuhjYClwAEBGbJK0G7gN6gcURsb/E+MzMrEJpSSEiHgJeUKV8FzCvxjzLgeVlxWRmZgPzP5rNzCznpGBmZjknBTMzyx10UpA0VdLzywjGzMwaq64TzZK6gNel+vcAv5R0e0R8oMTYzGwUqLwP9JI5vVX/mHeofC/o0aHePYXJEfEE8GfAv0XEXOCc8sIyM7NGqDcpTEz/Pn4j8I0S4zEzswaqNyl8DLgF2BwRd0k6GXiwvLDMzKwR6v3z2qMRkZ9cjoiHJH2qpJjMSlV5jNzMfq/ePYXP1llmZmZNbMA9BUlnAy8BTpBUvNLoWMB3RTMzG2MGO3x0ONCS6h1TKH8CeENZQZmZWWMMmBQi4nbgdklfjIifj1BMZmbWIPWeaD5C0gpgZnGeiPiTMoIyM7PGqDcpfA34AnAV4HscmJmNUfUmhd6I+HypkZiZWcPVe0nq1yX9haRpko7re5QamZmZjbh69xT67qn8wUJZACcPbzhmZtZIde0pRMRJVR51JQRJEyT9UNI30vhxkm6V9GB6nlqoe6mkzZIekHTu0JpkZmZDVW/X2W+rVh4RX6pj9vcB95P94Q1gKbAuIi6TtDSNf0jSacACYDbwTOA2Sc+NCJ/YNjMbIfWeUziz8PhjYBnZ/RUGJGkG8Gqyq5b6zAdWpuGVwPmF8s6I2BcRDwObgbPqjM/MzIaBIuLgZ5ImA1+OiAETg6Q1wMfJ/g39lxHxGkl7ImJKoc7uiJgq6QrgjohYlcqvBm6OiDUVy1wELAJobW2d29nZedDxH4yenh5aWlpKXUfZxkIbYPjasXH748MQzdC0ToLuvQ1b/bAoqw1zpk8e/oXWMBY+E4fSho6Ojg0R0VZtWr0nmiv9Bpg1UAVJrwF2RsQGSe11LFNVyvplrIhYAawAaGtri/b2ehY9dF1dXZS9jrKNhTbA8LWjjLuG1WvJnF4u3zjUj93oUFYbtlzYPuzLrGUsfCbKakO95xS+zu+/oCcAzwNWDzLbS4HXSXoVcCRwrKRVQLekaRHxaLpxz85UfxtwYmH+GcCO+pphZmbDod50/8nCcC/w84jYNtAMEXEpcClA2lP4y4h4i6RPkF3iell6vjHNshb4arpPwzPJ9kTW1xmfmZkNg7qSQkTcLqmV7EQzHNpd1y4DVku6GNgKXJDWsUnSauA+ssSz2FcemZmNrHoPH70R+ATQRXbs/7OSPlh5EriWiOhK8xIRu4B5NeotB5bXs0wzMxt+9R4++ghwZkTsBJB0AnAbUFdSMDOz5lDv/xSe1pcQkl0HMa+ZmTWJevcUvinpFuDaNP4m4D/KCcnMzBplsHs0nwK0RsQHJf0Z8Edk5xS+D3xlBOIzM7MRNNghoM8AvwaIiOsj4gMR8X6yvYTPlB2cmZmNrMGSwsyI+HFlYUTcTXZrTjMzG0MGSwpHDjBt0nAGYmZmjTdYUrhL0jsrC9MfzzaUE5KZmTXKYFcfXQLcIOlCfp8E2oDDgdeXGZiZmY28AZNCRHQDL5HUAZyeim+KiP8sPTIzMxtx9fZ99G3g2yXHYmZmDeZ/JZuZWc5JwczMck4KZmaWc1IwM7Ock4KZmeWcFMzMLFdaUpB0pKT1kn4kaZOkj6Xy4yTdKunB9Dy1MM+lkjZLekDSuWXFZmZm1ZW5p7AP+JOIeAFwBnCepBcDS4F1ETELWJfGkXQasACYDZwHXClpQonxmZlZhdKSQmR60uhh6RHAfGBlKl8JnJ+G5wOdEbEvIh4GNgNnlRWfmZn1p4gob+HZL/0NwCnA5yLiQ5L2RMSUQp3dETFV0hXAHRGxKpVfDdwcEWsqlrkIWATQ2to6t7Ozs7T4AXp6emhpaSl1HWUbC22A4WvHxu2PD0M0Q9M6Cbr3Nmz1w6KsNsyZPnn4F1rDWPhMHEobOjo6NkREW7Vp9d6Oc0giYj9whqQpZB3rnT5AdVVbRJVlrgBWALS1tUV7e/twhFpTV1cXZa+jbGOhDTB87bho6U2HHswQLZnTy+UbS/3Yla6sNmy5sH3Yl1nLWPhMlNWGEbn6KCL2AF1k5wq6JU0DSM87U7VtwImF2WYAO0YiPjMzy5R59dEJaQ8BSZOAc4CfAGuBhanaQuDGNLwWWCDpCEknAbOA9WXFZ2Zm/ZW5HzsNWJnOKzwNWB0R35D0fWB1ulHPVuACgIjYJGk1cB/QCyxOh5/MzGyElJYU0r2d/7BK+S5gXo15lgPLy4rJzMwG5n80m5lZzknBzMxyTgpmZpZzUjAzs5yTgpmZ5ZwUzMws56RgZmY5JwUzM8s5KZiZWc5JwczMck4KZmaWc1IwM7Ock4KZmeWcFMzMLOekYGZmOScFMzPLOSmYmVnOScHMzHKlJQVJJ0r6tqT7JW2S9L5UfpykWyU9mJ6nFua5VNJmSQ9IOres2MzMrLoy9xR6gSUR8TzgxcBiSacBS4F1ETELWJfGSdMWALOB84ArJU0oMT4zM6tQWlKIiEcj4gdp+NfA/cB0YD6wMlVbCZyfhucDnRGxLyIeBjYDZ5UVn5mZ9aeIKH8l0kzgO8DpwNaImFKYtjsipkq6ArgjIlal8quBmyNiTcWyFgGLAFpbW+d2dnaWGntPTw8tLS2lrqNsY6ENMHzt2Lj98WGIZmhaJ0H33oatfliU1YY50ycP/0JrGAufiUNpQ0dHx4aIaKs2beIhRVUHSS3AvwOXRMQTkmpWrVLWL2NFxApgBUBbW1u0t7cPU6TVdXV1UfY6yjYW2gDD146Llt506MEM0ZI5vVy+sfSPXanKasOWC9uHfZm1jIXPRFltKPXqI0mHkSWEr0TE9am4W9K0NH0asDOVbwNOLMw+A9hRZnxmZnagMq8+EnA1cH9EfKowaS2wMA0vBG4slC+QdISkk4BZwPqy4jMzs/7K3I99KfBWYKOke1LZh4HLgNWSLga2AhcARMQmSauB+8iuXFocEftLjM/MzCqUlhQi4ntUP08AMK/GPMuB5WXFZGZmA/M/ms3MLOekYGZmOScFMzPLOSmYmVnOScHMzHJOCmZmlnNSMDOzXHN3wmJjzswB+iVaMqe3of0WmY0H3lMwM7Oc9xTMbFQYaC9xuGy57NWlr6PZeU/BzMxyTgpmZpZzUjAzs5yTgpmZ5ZwUzMws56RgZmY5JwUzM8uV9j8FSdcArwF2RsTpqew44DpgJrAFeGNE7E7TLgUuBvYD742IW8qKzYZmJK4jN7PGKnNP4YvAeRVlS4F1ETELWJfGkXQasACYnea5UtKEEmMzM7MqSksKEfEd4FcVxfOBlWl4JXB+obwzIvZFxMPAZuCssmIzM7PqFBHlLVyaCXyjcPhoT0RMKUzfHRFTJV0B3BERq1L51cDNEbGmyjIXAYsAWltb53Z2dpYWP0BPTw8tLS2lrqNsw9WGjdsfH4Zohq51EnTvbWgIh8xtaKw50ycD/lx3dHRsiIi2atNGS99HqlJWNVtFxApgBUBbW1u0t7eXGBZ0dXVR9jrKNlxtaHQPpUvm9HL5xtHylh0at6GxtlzYDvhzPZCRvvqoW9I0gPS8M5VvA04s1JsB7Bjh2MzMxr2RTgprgYVpeCFwY6F8gaQjJJ0EzALWj3BsZmbjXpmXpF4LtAPHS9oGfBS4DFgt6WJgK3ABQERskrQauA/oBRZHxP6yYjMzs+pKSwoR8eYak+bVqL8cWF5WPGZmNjj/o9nMzHLNeQmBmdkQ9P0rv+z7fTfzHd68p2BmZjknBTMzyzkpmJlZzknBzMxyTgpmZpZzUjAzs5yTgpmZ5ZwUzMws56RgZmY5JwUzM8u5m4sxYOYgf9cv+y/9ZjZ2eE/BzMxyTgpmZpZzUjAzs5zPKZRssOP9ZmajifcUzMwsN+qSgqTzJD0gabOkpY2Ox8xsPBlVh48kTQA+B/wpsA24S9LaiLivjPXVc2jHl3Oa2cEaicPGXzzv6FKWO9r2FM4CNkfEQxHxFNAJzG9wTGZm44YiotEx5CS9ATgvIt6Rxt8KvCgi3l2oswhYlEZPBR4oOazjgcdKXkfZxkIbYGy0w20YHcZ7G54dESdUmzCqDh8BqlJ2QNaKiBXAipEJByTdHRFtI7W+MoyFNsDYaIfbMDq4DbWNtsNH24ATC+MzgB0NisXMbNwZbUnhLmCWpJMkHQ4sANY2OCYzs3FjVB0+ioheSe8GbgEmANdExKYGhzVih6pKNBbaAGOjHW7D6OA21DCqTjSbmVljjbbDR2Zm1kBOCmZmlnNSqCBpi6SNku6RdHcqWyZpeyq7R9KrGh3nQCRNkbRG0k8k3S/pbEnHSbpV0oPpeWqj4xxIjTY0zXaQdGohznskPSHpkmbaDgO0oWm2A4Ck90vaJOleSddKOrKZtgPUbEMp28HnFCpI2gK0RcRjhbJlQE9EfLJRcR0MSSuB70bEVekqrqOADwO/iojLUp9SUyPiQw0NdAA12nAJTbQd+qTuW7YDLwIW00TboU9FG95Ok2wHSdOB7wGnRcReSauB/wBOo0m2wwBtmEkJ28F7CmOMpGOBlwFXA0TEUxGxh6y7kJWp2krg/MZEOLgB2tCs5gE/i4if00TboUKxDc1mIjBJ0kSyHxc7aL7tUK0NpXBS6C+Ab0nakLrU6PNuST+WdM0o39U8Gfgl8G+SfijpKklHA60R8ShAen5GI4McRK02QPNsh6IFwLVpuJm2Q1GxDdAk2yEitgOfBLYCjwKPR8S3aKLtMEAboITt4KTQ30sj4oXAK4HFkl4GfB54DnAG2Ua5vIHxDWYi8ELg8xHxh8CTQLN1QV6rDc20HQBIh75eB3yt0bEMVZU2NM12SF+U84GTgGcCR0t6S2OjOjgDtKGU7eCkUCEidqTnncANwFkR0R0R+yPid8C/kvXmOlptA7ZFxJ1pfA3ZF2y3pGkA6Xlng+KrR9U2NNl26PNK4AcR0Z3Gm2k79DmgDU22Hc4BHo6IX0bEb4HrgZfQXNuhahvK2g5OCgWSjpZ0TN8w8Arg3r43T/J64N5GxFePiPgF8IikU1PRPOA+su5CFqayhcCNDQivLrXa0EzboeDNHHjYpWm2Q8EBbWiy7bAVeLGkoySJ7L10P821Haq2oazt4KuPCiSdTLZ3ANkhjK9GxHJJXybbRQtgC/CuvuORo5GkM4CrgMOBh8iuFnkasBp4Ftmb7IKI+FXDghxEjTb8M821HY4CHgFOjojHU9nTaa7tUK0NzfZ5+BjwJqAX+CHwDqCF5toO1dpwFSVsBycFMzPL+fCRmZnlnBTMzCznpGBmZjknBTMzyzkpmJlZblTdec1sOKXLP9el0T8A9pN1nwHZnxKfakhgVUhqB56KiP9udCw2vjkp2JgVEbvIruMeFT3dSpoYEeP4oy0AAAJZSURBVL01JrcDPUDdSUHShIjYPxyxmfXx4SMbVyTNlXR76vDwlkJXB12SPi3pO8ru33CmpOtTf/t/n+rMVHZ/h5WpE7I16c9dgy33HyTdDrxP0msl3Zk6+rtNUqukmcCfA+9P/eL/saQvSnpDIe6e9Nwu6duSvgpslDRB0ick3ZVietdIvp429jgp2Hgi4LPAGyJiLnANsLww/amIeBnwBbJuDxYDpwMXpUNRAKcCKyLi+cATwF9IOmyQ5U6JiJdHxOVk/eK/OHX01wn8VURsSev8dEScERHfHaQdZwEfiYjTgIvJes08EzgTeKekkw7+pTHL+PCRjSdHkH3J35p1IcMEst4l+6xNzxuBTX1dBkh6CDgR2AM8EhH/leqtAt4LfHOQ5V5XGJ4BXJf2JA4HHh5CO9ZHRN98rwCeX9irmAzMGuJyzZwUbFwR2Zf92TWm70vPvysM9433fVYq+4WJOpb7ZGH4s8CnImJtOrm8rMY8vaQ9+dQJ2uE1lifgPRFxS43lmB0UHz6y8WQfcIKkswEkHSZp9kEu41l985P1Hvo94IGDWO5ksttawu976QT4NXBMYXwLMDcNzwcOq7G8W4D/nQ5hIem5hRsSmR00JwUbT34HvAH4R0k/Au4h61v/YNwPLJT0Y+A4shsBPXUQy10GfE3Sd4HHCuVfB17fd6KZrH/8l0taT3Zf5Cf7LSlzFVnX6D+QdC/wL/gIgB0C95JqVqd0ldA3IuL0BodiVhrvKZiZWc57CmZmlvOegpmZ5ZwUzMws56RgZmY5JwUzM8s5KZiZWe7/A8XfY2oaIIllAAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "#plot histogram\n",
    "plt.hist(tobsdf['tobs'], bins=12)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "#plot labels\n",
    "plt.xlabel('Temperature')\n",
    "plt.ylabel('Counts')\n",
    "plt.title('Temperature Measurement Counts')\n",
    "\n",
    "#plt.ylim(0, max(groupdf[tobs])+5)\n",
    "#plt.xlim(min(tobs_count[0])-2, max(tobs_count[0])+2)\n",
    "\n",
    "#show plot with grid\n",
    "plt.grid(True)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 80,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with windowsapi reloader\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, jsonify\n",
    "\n",
    "\n",
    "# Flask Setup\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Flask Routes\n",
    "\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    print(\"List all available api route.\")\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/station<br/>\"\n",
    "        f\"/api/v1.0/measurement\"\n",
    "    )\n",
    "\n",
    "\n",
    "@app.route(\"/api/v1.0/station\")\n",
    "def stations():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    print(\"Return a list of all stations\")\n",
    "    # Query all stations\n",
    "    results = session.query(stations.station, station.name, station.latitude, station.longitude, station.elevation).all()\n",
    "    session.close()\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all_stations\n",
    "    all_stations = []\n",
    "    for station, name, latitude, longitude, elevations in results:\n",
    "        stations_dict = {}\n",
    "        stations_dict[\"station\"] = station\n",
    "        stations_dict[\"name\"] = name\n",
    "        stations_dict[\"laltitude\"] = latitude\n",
    "        stations_dict[\"longitude\"] = longitude\n",
    "        stations_dict[\"elevation\"] = elevation\n",
    "        all_stations.append(passenger_dict)\n",
    "\n",
    "    return jsonify(all_stations)\n",
    "\n",
    "\n",
    "\n",
    "@app.route(\"/api/v1.0/measurements\")\n",
    "def measurements():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    print(\"Return a list of passenger data including the name, age, and sex of each passenger\")\n",
    "    # Query all Measurements\n",
    "    results = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all_measurements\n",
    "    all_measurements = []\n",
    "    for station, date, prcp, tobs in results:\n",
    "        measurements_dict = {}\n",
    "        measurements_dict[\"station\"] = station\n",
    "        measurements_dict[\"date\"] = date\n",
    "        measurements_dict[\"prcp\"] = prcp\n",
    "        measurements_dict[\"tobs\"] = tobs\n",
    "        all_measurements.append(passenger_dict)\n",
    "\n",
    "    return jsonify(all_measurements)\n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' \n",
    "# and return the minimum, average, and maximum temperatures for that range of dates\n",
    "def calc_temps(start_date, end_date):\n",
    "    \"\"\"TMIN, TAVG, and TMAX for a list of dates.\n",
    "    \n",
    "    Args:\n",
    "        start_date (string): A date string in the format %Y-%m-%d\n",
    "        end_date (string): A date string in the format %Y-%m-%d\n",
    "        \n",
    "    Returns:\n",
    "        TMIN, TAVE, and TMAX\n",
    "    \"\"\"\n",
    "    \n",
    "    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "\n",
    "# function usage example\n",
    "print(calc_temps('2012-02-28', '2012-03-05'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax \n",
    "# for your trip using the previous year's data for those same dates.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plot the results from your previous query as a bar chart. \n",
    "# Use \"Trip Avg Temp\" as your Title\n",
    "# Use the average temperature for the y value\n",
    "# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.\n",
    "# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[(62.0, 69.15384615384616, 77.0)]"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Create a query that will calculate the daily normals \n",
    "# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)\n",
    "\n",
    "def daily_normals(date):\n",
    "    \"\"\"Daily Normals.\n",
    "    \n",
    "    Args:\n",
    "        date (str): A date string in the format '%m-%d'\n",
    "        \n",
    "    Returns:\n",
    "        A list of tuples containing the daily normals, tmin, tavg, and tmax\n",
    "    \n",
    "    \"\"\"\n",
    "    \n",
    "    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "    return session.query(*sel).filter(func.strftime(\"%m-%d\", Measurement.date) == date).all()\n",
    "    \n",
    "daily_normals(\"01-01\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "# calculate the daily normals for your trip\n",
    "# push each tuple of calculations into a list called `normals`\n",
    "\n",
    "# Set the start and end date of the trip\n",
    "\n",
    "# Use the start and end date to create a range of dates\n",
    "\n",
    "# Stip off the year and save a list of %m-%d strings\n",
    "\n",
    "# Loop through the list of %m-%d strings and calculate the normals for each date\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plot the daily normals as an area plot with `stacked=False`\n"
   ]
  }
 ],
 "metadata": {
  "kernel_info": {
   "name": "python3"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  },
  "nteract": {
   "version": "0.12.3"
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
