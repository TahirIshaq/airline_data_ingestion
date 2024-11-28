"""Uploads the data setes to S3"""
import os
from datetime import datetime
from airflow.models import Variable
from airflow.decorators import dag, task, task_group
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

S3_BUCKET = Variable.get("s3_bucket")
BASE_PATH = "/opt/airflow/dags"
AWS_CONN_ID = "upload_to_s3"

default_args = {
    "owner": "Tahir Ishaq",
    "email": "tahirishaq10@gmail.com"
}

@dag(
    dag_id = "upload_dataset",
    description = "Uploads the data sets to S3",
    default_args = default_args,
    start_date = datetime(2024, 10, 22),
    schedule_interval = None,
    catchup = False,
    tags = ["extract", "dataset"]
)
def upload_dataset():

    create_bucket = S3CreateBucketOperator(
        aws_conn_id=AWS_CONN_ID,
        task_id="create_bucket",
        bucket_name=S3_BUCKET,
    )

    @task_group(group_id="upload_files")
    def upload_files():
        """Upload multiple files to S3"""
        
        def files_to_upload(d_name="dags", f_ext=".csv"):
            """Get the file names to upload"""
            return [f_name for f_name in os.listdir(d_name) if f_name.endswith(f_ext)]
    
        data_path = os.path.abspath(f"{BASE_PATH}/data")
        files_list = files_to_upload(d_name=data_path, f_ext=".csv")
        
        upload_multiple_files = []
        for idx, f_name in enumerate(files_list):
            upload_multiple_files.append(
                LocalFilesystemToS3Operator(
                    task_id = f"upload_file{idx}",
                    aws_conn_id=AWS_CONN_ID,
                    filename=f"{BASE_PATH}/data/{f_name}",
                    dest_key=f_name,
                    dest_bucket=S3_BUCKET,
                    replace=True
                )
            )
        # filename argument does not recognize the path if passed from a local variable

        upload_multiple_files

    create_bucket >> upload_files()

dag = upload_dataset()