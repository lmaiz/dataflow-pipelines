import apache_beam as beam
from apache_beam.options.pipeline_options import (
    GoogleCloudOptions,
    PipelineOptions,
    SetupOptions,
    StandardOptions,
)
from apache_beam.transforms.window import FixedWindows
from apache_beam.io.fileio import MatchAll

from app.runtime_options import RuntimeOptions
from app.utils import GeneratePath
from app.schema import POKEMON_SCHEMA
from app.utils import PokemonProcessing

def run(argv=None):
    pipeline_options = PipelineOptions()
    project_id = str(pipeline_options.view_as(GoogleCloudOptions).project)
    service_account_email = pipeline_options.view_as(
        GoogleCloudOptions
    ).service_account_email
    pipeline_options.view_as(SetupOptions).save_main_session = True
    runtime_options = pipeline_options.view_as(RuntimeOptions)

    # Fetch common parameters
    mode = runtime_options.mode
    dataset = runtime_options.dataset
    table_name = runtime_options.table_name

    pipeline_options.view_as(StandardOptions).streaming = (
        True if mode == "streaming" else False
    )

    try:
        with beam.Pipeline(options=pipeline_options) as p:
            if mode == "batch":
                # Fetch specific parameters for the batch pipeline
                bucket_name = runtime_options.bucket_name
                file_path = runtime_options.file_path

                input = (
                    p
                    | "[Batch] Pipeline init" >> beam.Create([None])
                    | "[Batch] Generate input files path"
                    >> beam.ParDo(
                        GeneratePath(
                            bucket_name=bucket_name,
                            file_path=file_path,
                        )
                    )
                    | "[Batch] Match files GCS bucket" >> MatchAll()
                    | "[Batch] Read matched files from GCS bucket" >> beam.io.textio.ReadAllFromText()
                )
    
            elif mode == "streaming":
                # Fetch specific parameters for the streaming pipeline
                pubsub_subscription = runtime_options.pubsub_subscription

                input = (
                    p
                    | "[Streaming] Pull PubSub Messages" >> beam.io.gcp.pubsub.ReadFromPubSub(subscription=f"projects/{project_id}/subscriptions/{pubsub_subscription}")
                    | "[Streaming] Apply Fixed Windows" >> beam.WindowInto(FixedWindows(60))
                    | '[Streaming] Decode Message' >> beam.Map(lambda msg: msg.decode('utf-8'))
                )

          
            write_to_bq = (
                input
                | PokemonProcessing()
                | "Write to a BQ table" >> beam.io.WriteToBigQuery(
                    table=table_name,
                    dataset=dataset,
                    project=project_id,
                    schema={"fields": POKEMON_SCHEMA},
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                )
            )

    except AssertionError:
        pass
