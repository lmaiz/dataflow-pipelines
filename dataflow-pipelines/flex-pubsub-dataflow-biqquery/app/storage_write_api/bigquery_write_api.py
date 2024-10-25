from google.cloud.bigquery_storage_v1 import types
from google.cloud.bigquery_storage_v1 import writer
from google.protobuf import descriptor_pb2

from app.storage_write_api import data_model_pb2

SINGULAR_FIELDS_TO_CHECK = [
    "session_id",
    "mpid",
    "session_start_time",
    "session_end_time",
    "session_duration",
    "ip",
    "country_iso2",
    "store_code",
    "dispatch_id",
    "variant_id",
    "utm_campaign",
    "utm_medium",
    "utm_source",
    "activity_platform",
    "operating_system",
    "update_date",
    "update_user",
    "_CHANGE_TYPE",
]


def create_row_data(data):
    row = data_model_pb2.DataModel()
    for field in SINGULAR_FIELDS_TO_CHECK:
        if field in data and data[field] is not None:
            setattr(row, field, data[field])
    return row.SerializeToString()


# Use the Storage Write API default stream to stream data into BigQuery.
# This mode uses at-least once delivery
# The stream name is: projects/{project}/datasets/{dataset}/tables/{table}/_default
class BigQueryStorageWriteAPI:
    def __init__(self, project_id: str, dataset_id: str, table_id: str, write_client):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.write_client = write_client

    def append_rows_proto2(self, data: dict):
        parent = self.write_client.table_path(
            self.project_id, self.dataset_id, self.table_id
        )
        stream_name = f"{parent}/_default"
        types.WriteStream()

        # Create a template with fields needed for the first request.
        request_template = types.AppendRowsRequest()
        # The request must contain the stream name.
        request_template.write_stream = stream_name

        # So that BigQuery knows how to parse the serialized_rows, generate a
        # protocol buffer representation of your message descriptor.
        proto_schema = types.ProtoSchema()
        proto_descriptor = descriptor_pb2.DescriptorProto()
        data_model_pb2.DataModel.DESCRIPTOR.CopyToProto(proto_descriptor)
        proto_schema.proto_descriptor = proto_descriptor
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.writer_schema = proto_schema
        request_template.proto_rows = proto_data
        # Some stream types support an unbounded number of requests. Construct an
        # AppendRowsStream to send an arbitrary number of requests to a stream.
        append_rows_stream = writer.AppendRowsStream(
            self.write_client, request_template
        )

        # Calls the create_row_data function to append proto2 serialized bytes to the
        # serialized_rows repeated field.
        proto_rows = types.ProtoRows()
        for row in data:
            proto_rows.serialized_rows.append(create_row_data(row))
        # Appends data to the given stream.
        request = types.AppendRowsRequest()
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.rows = proto_rows
        request.proto_rows = proto_data
        append_rows_stream.send(request)
        append_rows_stream.close()
