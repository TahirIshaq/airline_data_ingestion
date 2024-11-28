import pandas as pd
from sqlalchemy import create_engine
import os


def connect_to_db(user, password, host, port, db_name):
    """Connect to the DB server and return the cursor"""
    login = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(login)
    return engine


def file_name_wo_ext(full_name):
    """Returns file name without extension"""
    end_idx = full_name.find(".")
    name = full_name[:end_idx]
    return name


def main():
    user = os.getenv("PG_USER", "dwh_user")
    password = os.getenv("PG_USER", "dwh_pass")
    host = os.getenv("PG_USER", "localhost")
    port = os.getenv("PG_USER", "5432")
    db_name = os.getenv("PG_USER", "dwh_db")

    engine = connect_to_db(user, password, host, port, db_name)
    dataset_dir = "Airline_Data_Ingestion_Project"
    datasets = [ds for ds in os.listdir(dataset_dir) if ds.endswith(".csv")]

    for data in datasets:
        with engine.connect() as con:
            df = pd.read_csv(os.path.abspath(os.path.join(dataset_dir, data)))
            table_name = file_name_wo_ext(data)
            df.to_sql(con=con, name=table_name, schema="public", if_exists="replace", index=False)
            print(f"Inserted {len(df)} rows in table \"{table_name}\"")


if __name__ == "__main__":
    main()