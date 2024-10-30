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
            "--bucket_name",
            help="Bucket",
        )
        parser.add_argument(
            "--file_path",
            help="Path",
        )
        parser.add_argument(
            "--pubsub_subscription",
            help="Subscription",
        )
        parser.add_argument(
            "--dataset",
            required=True,
            help="Dataset",
        )
        parser.add_argument(
            "--table_name",
            required=True,
            help="Table Name",
        )
