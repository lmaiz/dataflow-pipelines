from apache_beam.options.pipeline_options import PipelineOptions


class RuntimeOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            "--mode",
            required=True,
            help="Pipeline mode (batch or streaming)",
        )
        parser.add_argument(
            "--destination_project_id",
            required=True,
            help="Google project in which bq tables are stored",
        )
        parser.add_argument(
            "--dataset",
            required=True,
            help="dataset",
        )
        parser.add_argument(
            "--dataset_errors",
            required=True,
            help="Error dataset",
        )
        parser.add_argument(
            "--table",
            required=True,
            help="BQ table",
        )
        parser.add_argument(
            "--bucket_name",
            help="GCS bucket name",
        )
        parser.add_argument(
            "--pubsub_subscription",
            help="PubSub sub",
        )
