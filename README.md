# Technical Showcase - Portfolio Analysis Tool
This project is the prototype of a portfolio analysis tool.

## How to set it up

The project can be set up by running `docker-compose up` on the root of the project's folder. Docker must be installed.
A Django-based web service will be spun up (see 0.0.0.0:8000), along with a PostgreSQL database, a Celery worker, the Celery beat that handles recurrent tasks, and a Flower dashboard (see ...), along with a Redis instance that enables the Celery tasks.

Upon first boot, the fixtures with a predefined set of assets and historic values will be added to the database. A superuser
with username and password `admin` will also be added to ease access to the admin site (see 0.0.0.0:8000/admin). For more information on the database tables and their relationship, see [Database Models](#database-models).

## Database Models

A __Portfolio__ is a collection of investments that is subject to recurrent analysis. It belongs to a particular __User__, the only one who can modify the information contained on it.

Each Portfolio contains several __Investment__s, which specify the Asset and the amount (i.e., number of shares) of it contained in the Portfolio.

The __Asset__ is the securities that are purchased under a portfolio by means of an Investment. It has a unique symbol, and a name, and belongs to a certain sector. The value of the asset is subject to change in time, and thus the information related to that historical change is stored in __HistoricValue__. The information retrieved from market data's API such as [Polygon](https://polygon.io/) is stored in this table.

## Endpoints

There are two main endpoints in this project: `/portfolios` and `/portfolio/<int:id>/sectors`. Feel free to explore them in [0.0.0.0:8000](http://0.0.0.0:8000/) in the API dashboard.

- `/portfolios`: GET all the portfolios. For simplicity, restrictions to only show portfolios to the authorised user have been left out of scope, so that an unauthorised user can, for now, see all portfolios. You can also see the information for a specific portfolio (See [0.0.0.0:8000/portfolios/1/](http://0.0.0.0:8000/portfolios/1/) for an example) An authorised user can also POST a new portfolio. See [0.0.0.0:8000/portfolios/](http://0.0.0.0:8000/portfolios/)

- `/portfolios/<int:id>/sectors`: GET a consolidated view of a certain portfolio investments grouped by sectors. See [0.0.0.0:8000/portfolios/1/sectors/](http://0.0.0.0:8000/portfolios/1/sectors/) for an example.

## Recurrent tasks

As part of the project, every day at 3am, the project is set to retrieve yesterday's market data for all assets in the system, and store them in the `HistoricValue` table. The architecture of this project favours storing data over retrieving that information in real time because of the rate limit of the API, and the subsequent latency derived from fetching the information from an external source. Besides, in the event of the Polygon API being down, this system would have been rendered useless. By storing all that information in the database, the *scalability* and the *resilience* of the system is improved.

## Items left out of scope, and future work.

As this is a prototype aimed at showcasing the possibilities of a Django-based portfolio analysis system, many items were left out of scope of the exercises. A non-exhaustive lists of those items can be found below.

- __Real time data__: Instead of relying on market data from the last day, the system may allow for the possibility to retrieve that information in real time, by means of Websockets.

The particular implementation wasn't specified, but Django allows for the usage of websockets by means of the [django-channels](https://channels.readthedocs.io/en/stable/) library. A new container would have to be spun up, which would rely on the already existing Redis container for memory management.

This `daphne` container would be tasked with creating, in real time, instances of Historic Value, which allows for the usage of datetimes, rather than dates, on the `date_time` column. To that end, it is likely that all other variables would have to be set to nullable, which will make historic analysis just a bit more complex.

- __Historic analysis and metrics__: Value at Risk, Sharpe Ratio, and other historic-centric indicators of the portfolio were left out of the scope, given the limitations of the free tier of the market data API. Should we have access to enough historical data, the system may include the possibility of displaying all those metrics in a similar fashion as the `/sectors` endpoint.

- __Alerts and Reports__: As part of the recurrent tasks, we can set up alerts that can be sent to the user's email when a certain treshold of risk is trespassed, or a monthly report of the evolution of the portfolio can be sent to potential clients. The implementation may involve a table of Customers that points to the __Portfolio__, and the related recurrent task would resemble that of the daily retrieval of historical information.

- __External Access__: This system is front-end agnostic, which means that it can be plugged seamlessly to a new or an existing website, enabling users to set themselves up without anyone else's involvement. In my opinion this should be the main focus of the system if it were to be implemented in production.

