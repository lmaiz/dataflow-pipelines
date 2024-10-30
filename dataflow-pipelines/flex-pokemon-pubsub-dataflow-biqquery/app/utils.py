import json
import logging

import apache_beam as beam

from .schema import POKEMON_SCHEMA

class GeneratePath(beam.DoFn):
    def __init__(self, bucket_name, file_path):
        self.bucket_name = bucket_name
        self.file_path = file_path

    def process(self, element):
        filename = f'gs://{self.bucket_name}/{self.file_path}'
        yield filename


class RecordCleaner(beam.DoFn):
    def process(self, element):
        data = element.strip().replace('}{','}}{{')
        data = data.split("}{")        
        for t in data:
            try:
                yield json.loads(t)
            except json.JSONDecodeError as error:
                logging.error(error)