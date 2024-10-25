import apache_beam as beam
from apache_beam.io.gcp.pubsub import ReadFromPubSub
from apache_beam.options.pipeline_options import (
    GoogleCloudOptions,
    PipelineOptions,
    SetupOptions,
    StandardOptions,
)
from apache_beam.transforms.window import FixedWindows
#from gborelpy.beam_utils import GeneratePath, ParseJSON
from app.runtime_options import RuntimeOptions


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
    destination_project_id = runtime_options.destination_project_id
    dataset = runtime_options.dataset
    dataset_errors = runtime_options.dataset_errors
    table = runtime_options.table

    pipeline_options.view_as(StandardOptions).streaming = (
        True if mode == "streaming" else False
    )

    try:
        with beam.Pipeline(options=pipeline_options) as p:
            data = None
            if mode == "batch":
                bucket_name = runtime_options.bucket_name
                input_date = "2024"
                data = (
                    p
                    | "Pipeline init" >> beam.Create([input_date])
                    # | "Generate input files path"
                    # >> beam.ParDo(
                    #     GeneratePath(
                    #         bucket=bucket_name,
                    #         files_prefix=None,
                    #         input_date=None,
                    #     )
                    # )
                    | "Show paths" >> beam.Map(print)
                    # | "[Session Start] Match files GCS bucket" >> MatchAll()
                    # | "[Session Start] Process Data" >> beam.ParDo(
                    #     ProcessData(
                    #         bucket_name,
                    #         destination_project_id,
                    #         dataset,
                    #         table,
                    #         dataset_errors,
                    #         SessionStartTemplate(service_account_email),
                    #         service_account_email,
                    #         job_name
                    #     )
                    # )
                    # | "[Session Start] Generate Completion Signal" >> beam.ParDo(CompletionMarker())
                )
            # elif mode == "streaming":
            #     data = (
            #         p
            #         | "[Streaming] Pull PubSub Messages"
            #         >> ReadFromPubSub(
            #             subscription=f"projects/{project_id}/subscriptions/{runtime_options.pubsub_subscription}"
            #         )
            #         | "[Streaming] Apply Fixed Windows"
            #         >> beam.WindowInto(FixedWindows(60))
            #         | "[Streaming] Parse Messages" >> beam.ParDo(ParseJSON())
            #         | "[Streaming] Show" >> beam.Map(lambda x: print(x))
            #         # | "[Session Start] Apply Session Start template"
            #         # >> beam.ParDo(SessionStartTemplate(service_account_email))
            #         # | "[Session Start] Upsert to BQ"
            #         # >> beam.ParDo(
            #         #     WriteToBQ(
            #         #         destination_project_id,
            #         #         dataset,
            #         #         table,
            #         #         dataset_errors,
            #         #         service_account_email,
            #         #     )
            #         # )
            #     )

            # session_end = (
            #     p
            #     | "[Session End] Pipeline init" >> beam.Create([None])
            #     | "[Session End] Wait for Session Start" >> beam.Map(lambda x, _: x, beam.pvalue.AsSingleton(session_start))
            #     | "[Session End] Generate input files path" >> beam.ParDo(GeneratePath(bucket=bucket_name, files_prefix="session_end"))
            #     | "[Session End] Match files GCS bucket" >> MatchAll()
            #     | "[Session End] Process Data" >> beam.ParDo(
            #         ProcessData(
            #             bucket_name,
            #             destination_project_id,
            #             dataset,
            #             table,
            #             dataset_errors,
            #             SessionEndTemplate(service_account_email),
            #             service_account_email,
            #             job_name
            #         )
            #     )
            # )

    except AssertionError:
        pass
