import sys
import unittest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

from app.utils import PokemonProcessing


class TestPokemonProcessing(unittest.TestCase):

  # Our input data, which will make up the initial PCollection.
  POKEMONS = [
     """{"Index":554,"Name":"Snivy","Type 1":"Grass","Type 2":null,"Total":308,"HP":45,"Attack":45,"Defense":55,"Special_Atk":45,"Special_Def":55,"Speed":63,"Generation":5,"Legendary":false}""",
     """{"Index":5,"Name":"Charmeleon","Type 1":"Fire","Type 2":null,"Total":405,"HP":58,"Attack":64,"Defense":58,"Special_Atk":80,"Special_Def":65,"Speed":80,"Generation":1,"Legendary":false}""",
     """{"Index":269,"Name":"Lugia","Type 1":"Psychic","Type 2":"Flying","Total":680,"HP":106,"Attack":90,"Defense":130,"Special_Atk":90,"Special_Def":154,"Speed":110,"Generation":2,"Legendary":true}"""
     ]


  # Our output data, which is the expected data that the final PCollection must match.
  EXPECTED_OUTPUTS = [
     {"pokemon_name": "Snivy","types": ["Grass"],"hp": 45,"attack": 45,"defense": 55,"special_atk": 45,"special_def": 55,"speed": 63,"generation_number": 5,"region": "Unys","legendary": False},
     {"pokemon_name": "Charmeleon","types": ["Fire"],"hp": 58,"attack": 64, "defense": 58, "special_atk": 80, "special_def": 65, "speed": 80, "generation_number": 1, "region": "Kanto", "legendary": False},
     {"pokemon_name": "Lugia","types": ["Psychic","Flying"],"hp": 106,"attack": 90, "defense": 130, "special_atk": 90, "special_def": 154, "speed": 110, "generation_number": 2, "region": "Johto", "legendary": True}
  ]


  def test_pokemon_processing(self):
    with TestPipeline() as p:

      # Create a PCollection from the POKEMONS static input data.
      input = p | beam.Create(self.POKEMONS)

      output = input | PokemonProcessing()

      # Assert that the output PCollection matches the EXPECTED_OUTPUTS data.
      assert_that(output, equal_to(self.EXPECTED_OUTPUTS), label='CheckOutput')


# Run the test
if __name__=="__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)
