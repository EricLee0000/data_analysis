import json
import numpy as np
import os
import pandas as pd
import pymysql
import psycopg2
from pathlib import Path

file_path = os.path.dirname(os.path.realpath(__file__))


def sql_query_to_pd(query, psql=False, db_name="DEFAULT"):
    with open(file_path + "/config.json", "r") as f:
        config = json.load(f)
    database = config[db_name]

    if psql is True:
        try:
            connection = psycopg2.connect(
                user=database["USER"],
                password=database["PASSWORD"],
                host=database["HOST"],
                port="5432",
                database=database["DB"],
            )
            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            return pd.read_sql_query(query, connection)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        connection = pymysql.connect(
            user=database["USER"],
            password=database["PASSWORD"],
            host=database["HOST"],
            db=database["DB"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.SSDictCursor,
        )
        try:
            return pd.read_sql(query, connection)

        finally:
            connection.close()


def sql_query_to_np(query, db_name="TINYPULSE_RO"):
    with open(file_path + "/config.json", "r") as f:
        config = json.load(f)
    database = config[db_name]
    connection = pymysql.connect(
        user=database["USER"],
        password=database["PASSWORD"],
        host=database["HOST"],
        db=database["DB"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.SSDictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = np.array(cursor.fetchall())
            return np.matrix([list(each.values()) for each in data])
    finally:
        connection.close()


def read_sql(base_dir, base_sql, **kwargs):
    sql = Path("%s/%s.sql" % (base_dir, base_sql)).read_text().format(**kwargs)
    return sql


def create_csv(FILEDIR, query, db_name, overwrite=False):
    """Check for existing csv and create/overwrite."""
    if not os.path.isfile(FILEDIR) or overwrite:
        df = sql_query_to_pd(query=query, db_name=db_name)
        df.to_csv(FILEDIR, index=None)
        print("Query ran. Csv file created")
    else:
        print("File already exists. Query skipped.")


def create_excel(FILEDIR, df, overwrite=False):
    """Check for existing csv and create/overwrite."""
    if not os.path.isfile(FILEDIR) or overwrite:
        df.to_excel(FILEDIR, index=None)
        print("File created.")
    else:
        print("File already exists. Skipped.")

    return pd.read_excel(FILEDIR)


if __name__ == "__main__":
    main()