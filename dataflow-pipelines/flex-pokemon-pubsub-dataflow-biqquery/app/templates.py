import apache_beam as beam

from .transformers import PokemonTransformer
import logging


class PokemonTemplate(beam.DoFn):

    def process(self, data):
        try:
            transformer = PokemonTransformer(data)
            logging.info(data)
            row = {
                "pokemon_name": transformer.pokemon_name,
                "types": transformer.types,
                "hp": transformer.hp,
                "attack": transformer.attack,
                "defense": transformer.defense,
                "special_atk": transformer.special_atk,
                "special_def": transformer.special_def,
                "speed": transformer.speed,
                "generation_number": transformer.generation_number,
                "region": transformer.region,
                "legendary": transformer.legendary
            }
            yield row
        except Exception as e:
            logging.error(
                "The following error occuried while creating PokemonTemplate : ",
                str(e),
            )
