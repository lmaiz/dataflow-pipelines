import json
import logging

import apache_beam as beam
from google.cloud import bigquery, bigquery_storage_v1, storage
from google.cloud.exceptions import NotFound

from .schema import SESSION_ERROR_SCHEMA, SESSION_SCHEMA
from .storage_write_api.bigquery_write_api import BigQueryStorageWriteAPI


class CompletionMarker(beam.DoFn):
    """
    Emit a completion marker to signal the end of a step.
    """

    def process(self, element):
        yield None


class ProcessData(beam.DoFn):
    """
    Process data from GCS, transform it using template, and write to BigQuery SESSION table.
    Archive successfully processed files to archive/ folder and move corrupted files to error/ foler in GCS

    Args:
        bucket (str): input GCS bucket
        destination_project_id (str): Google Cloud project ID for BigQuery
        dataset (str): BigQuery dataset name
        table (str): BigQuery table name
        dataset_errors (str): BigQuery error dataset name
        template (obj): Processing template
        service_account_email (str): Service account email
        job_name (str): Job name
    """

    def __init__(
        self,
        bucket,
        destination_project_id,
        dataset,
        table,
        dataset_errors,
        template,
        service_account_email,
        job_name,
    ):
        self.bucket = bucket
        self.bq_project = destination_project_id
        self.dataset = dataset
        self.bq_table = table
        self.error_dataset = dataset_errors
        self.error_bq_table = table
        self.template = template
        self.service_account_email = service_account_email
        self.job_name = job_name

    def setup(self):
        self.storage_client = storage.Client(project=self.bq_project)
        self.bigquery_client = bigquery.Client(project=self.bq_project)
        self.required_fields = set()
        for field in SESSION_SCHEMA:
            if field["mode"].lower() == "required":
                self.required_fields.add(field["name"])
        self.bq_storage_client = bigquery_storage_v1.BigQueryWriteClient()
        self.bq_writer = BigQueryStorageWriteAPI(
            self.bq_project, self.dataset, self.bq_table, self.bq_storage_client
        )
        create_bq_table(
            self.bigquery_client,
            f"{self.bq_project}.{self.error_dataset}.{self.error_bq_table}",
            SESSION_ERROR_SCHEMA,
        )
        self.archive_gcs_folder = f"archive/{self.job_name}"
        self.error_gcs_folder = f"error/{self.job_name}"

    def process(self, file_meta):
        try:
            # Read and parse files
            path_parts = file_meta.path.replace("gs://", "").split("/", 1)
            file_key = path_parts[1]
            content = read_gs_content(self.storage_client, self.bucket, file_key)
            data = content.strip()
            data = data.split("\n")
            data = [json.loads(t) for t in data]

            # Process the data
            processed_data = [self.template.process(t) for t in data]

            # Split the data into valid and invalid data (Null mandatory fields)
            valid_data, invalid_data = split_null_mandatory_data(
                processed_data, self.required_fields
            )

            # Upsert valid data to Return table using the BQ Storage Write API
            if len(valid_data) > 0:
                self.bq_writer.append_rows_proto2(valid_data)

            if len(invalid_data) > 0:  # If invalid data found
                logging.error("Invalid data : null mandatory fields")
                # Insert data to bq error table using the BQ Streaming API
                self.bigquery_client.insert_rows_json(
                    table=f"{self.bq_project}.{self.error_dataset}.{self.error_bq_table}",
                    json_rows=invalid_data,
                )

                # Copying the source file to error/ GCS folder
                copy_blob(
                    self.storage_client,
                    self.bucket,
                    file_key,
                    f"{self.error_gcs_folder}/{file_key}",
                )
                logging.error(
                    f"File moved from {file_key} to {self.error_gcs_folder}/{file_key}"
                )
            else:  # No invalid data / File with no invalid data
                # Copying the source file to archive/ GCS folder
                copy_blob(
                    self.storage_client,
                    self.bucket,
                    file_key,
                    f"{self.archive_gcs_folder}/{file_key}",
                )
                logging.info(
                    f"Data from {file_key} has been successfully inserted into {self.bq_project}.{self.dataset}.{self.bq_table}"
                )
        except Exception as error:
            # Copying the source file to error/ GCS folder
            logging.error(f"An error occured : {error}")
            copy_blob(
                self.storage_client,
                self.bucket,
                file_key,
                f"{self.error_gcs_folder}/{file_key}",
            )
            logging.error(
                f"File moved from {file_key} to {self.error_gcs_folder}/{file_key}"
            )


def split_null_mandatory_data(data, required_fields):
    """
    Split data into valid and invalid based on presence of required fields.

    Args:
        data (list): List of data records.
        required_fields (set): Set of required fields.

    Returns:
        tuple: valid data list, invalid data list
    """
    valid = []
    invalid = []
    for element in data:
        is_valid = True
        for required_key in required_fields:
            if element[required_key] is None:
                is_valid = False

        if is_valid:
            valid.append(element)
        else:
            # Drop keys with None value and _CHANGE_TYPE key to insert instead of upsert
            element = {
                k: v
                for k, v in element.items()
                if (v is not None and k != "_CHANGE_TYPE")
            }
            invalid.append(element)

    return valid, invalid


def create_bq_table(bq_client, table_id, schema):
    """
    Create a BigQuery table if it doesn't exist.

    Args:
        bq_client (bigquery.Client): BigQuery client.
        table_id (str): BigQuery table ID.
        schema (list): BigQuery table schema.
    """
    try:
        bq_client.get_table(table_id)
    except NotFound:
        logging.info(f"Table {table_id} is not found. Creating ...")
        table = bigquery.Table(table_id, schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY
        )
        table = bq_client.create_table(table)
        logging.info(f"Table {table_id} created")


def read_gs_content(storage_client, bucket_name, file_key):
    """
    Read content from GCS.

    Args:
        storage_client (storage.Client): GCS storage client.
        bucket_name (str): GCS bucket name.
        file_key (str): File key in GCS bucket.

    Returns:
        str: Content of the file as a string.
    """
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_key)

    content = blob.download_as_string()

    return content.decode("utf-8")


def copy_blob(storage_client, bucket_name, blob_name, error_blob_name):
    """
    Copy a blob within GCS.

    Args:
        storage_client (storage.Client): GCS storage client.
        bucket_name (str): GCS bucket name.
        blob_name (str): Source blob name.
        error_blob_name (str): Destination blob name.
    """
    bucket = storage_client.bucket(bucket_name)

    source_blob = bucket.blob(blob_name)
    error_blob = bucket.blob(error_blob_name)

    if not error_blob.exists():
        bucket.copy_blob(source_blob, bucket, error_blob_name)
