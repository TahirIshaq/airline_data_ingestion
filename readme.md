# Objective
1. Upload datasets to S3
2. Perform transformaitons to the uploaded datasets and store the results in Redshift(PostgreSQL in this case).
3. In redshift, all tables should be created in a new schema
4. EDA should be performed on the raw data to create the schema of the tables that need to be created in Redshift
5. Another approach could be to just load the raw data as is in the data warehouse and then use DBT or similar tools to perform the transformations.


A pipeline that downloads weather [data](https://open-meteo.com/) and store it in postgres and S3.
After selecting the desired city and parameters, a URL will be generated that can used to query the selected parameters of the city selected above.

## Complete SQL code
```
WITH delayed_records AS
(
	SELECT *
	FROM flights
	WHERE "DepDelay" >= 60
),
dep_records AS
(
	SELECT
		CAST(f."Carrier" AS VARCHAR(50)) AS carrier,
		CAST(f."DepDelay" AS bigint) AS dep_delay,
		CAST(f."ArrDelay" AS bigint) AS arr_delay,
		CAST(f."DestAirportID" AS bigint) AS dest_airport_id,
		CAST(a.name AS VARCHAR(100)) AS dep_airport,
		CAST(a.state AS VARCHAR(50)) AS dep_state,
		CAST(a.city AS VARCHAR(50)) AS dep_city
	FROM delayed_records f
	LEFT JOIN airports a
	ON f."OriginAirportID" = a.airport_id
)
SELECT
	d.carrier,
	d.dep_delay,
	d.arr_delay,
	d.dep_airport,
	d.dep_state,
	d.dep_city,
	CAST(a.name AS VARCHAR(100)) AS arr_airport,
	CAST(a.state AS VARCHAR(50)) AS arr_state,
	CAST(a.city AS VARCHAR(50)) AS arr_city
FROM dep_records d
LEFT JOIN airports a
ON d.dest_airport_id = a.airport_id;
```


## How to run the project
```
git clone https://github.com/TahirIshaq/weather_data_elt
cd weather_data_elt
docker compose up -d
In a web browser open: "https://localhost:8080".
Trigger the DAG.
In another tab of the web browser open: "http://localhost:9001".
Check the file that was uploaded to the bucket.
Login to the postgres container by typing the following in the terminal: docker exec -it dwh bash
Login to the postgres server terminal by tying: psql "postgresql://dwh_user:dwh_pass@localhost:5432/dwh_db"
List the current tables in the database: \d
List the weather table schema: \d+ weather_data;
List the contents of weather table: SELECT * FROM weather_data;
Exit the postgres server terminal: type "exit" or ctrl + D
Exit the postgres server container: type "exit" or ctrl + D
Take down all the container: docker compose down
(optional)Take down all the containers, volumes and delete the docker images: docker compose down -v --rmi all
```

## Implementation
In airflow connectors of the destination database, API and AWS S3 need to be created.

## Airflow connection creation
In airfow UI connecitons need to be created for API, postgres and S3.

### Weather data API
Create a HTTP connection type with the following details:
| Key | Value |
| --- | --- |
| Connection Id | weather_api |
| Host | https://api.open-meteo.com |

### Postgres
Create a Postgres connection type with the following details:
| Key | Value |
| --- | --- |
| Connection Id | dwh |
| Host | dwh |
| Port | 5432 |
| Login | dwh_user |
| Password | dwh_pass |
| Database | dwh_db |

### S3
Create a Amazon Web Service connection type with following details:
| Key | Value |
| --- | --- |
| Connection Id | to_s3 |
| AWS Access Key ID | admin |
| AWS Secret Access Key | admin12345 |
| Extra | {"endpoint_url": "http://s3:9000"} |

## Test
```
docker exec -it dwh bash
psql "postgresql://dwh_user:dwh_pass@localhost:5432/dwh_db"
\d
\d+ weather_data
SELECT * FROM weather_data;
```

## To do
- [x] Add DAG test
- [ ] Use Airbyte or similar data loading software
- [ ] Use DBT to perform data transformations

## References
- [S3 file upload loop](https://stackoverflow.com/questions/70002086/how-to-run-tasks-sequentially-in-a-loop-in-an-airflow-dag)
- [SQL subqueries 1](https://mode.com/sql-tutorial/sql-sub-queries)
- [SQl subqueries 2](https://www.kaggle.com/code/alexisbcook/analytic-functions)
- [SQL casting](https://neon.tech/postgresql/postgresql-tutorial/postgresql-cast)
- [DBT SQl casting](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/taxi_rides_ny/models/core/fact_trips.sql)
- [Pandas df to sql](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html)
- [Airline Data Ingestion Project](https://www.youtube.com/watch?v=35Du026h-KY)
- [Airflow Python external operator](https://www.youtube.com/watch?v=mWQa5mWpMZ4)
- [Pyairbyte](https://www.youtube.com/watch?v=Ffb5xMQiJkY)



Old references
- [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html)
- [Airflow AWS Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)
- [Airflow S3 Operator](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/s3/index.html#airflow.providers.amazon.aws.operators.s3.S3CreateBucketOperator)
- [Postgres Connection](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/connections/postgres.html)
- [HTTP Connection](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/connections/http.html)
- [SQLExecuteQueryOperator dynamic input](https://arthurpedroti.com.br/how-to-create-your-first-etl-in-apache-airflow/)
- [SQLExecuteQueryOperator output](https://www.astronomer.io/blog/apache-airflow-taskflow-api-vs-traditional-operators/)
- [How to build and automate a python ETL pipeline with airflow on AWS EC2](https://www.youtube.com/watch?v=uhQ54Dgp6To)
- [Apache Airflow One Shot- Building End To End ETL Pipeline Using AirFlow And Astro](https://www.youtube.com/watch?v=Y_vQyMljDsE)
- [repo 1](https://github.com/YemiOla/data_engineering_project_openweathermap_api_airflow_etl_aws)
- [repo 2](https://github.com/krishnaik06/ETLWeather)# Objective
A pipeline that downloads weather [data](https://open-meteo.com/) and store it in postgres and S3.
After selecting the desired city and parameters, a URL will be generated that can used to query the selected parameters of the city selected above.

