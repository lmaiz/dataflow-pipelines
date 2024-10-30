from functools import cached_property

from app.constants import MAPPING_GENERATION_REGION

class PokemonTransformer:
    def __init__(self, data):
        self._data = data

    def get_pokemon_name(self) -> str:
        return self._data.get("Name")

    @cached_property
    def pokemon_name(self) -> str:
        """
        Get pokemon_name attribute
        """
        return self.get_pokemon_name()


    def get_types(self) -> list[str]:
        types = []
        if self._data.get("Type 1")!= None:
            types.append(self._data.get("Type 1"))
        if self._data.get("Type 2")!= None:
            types.append(self._data.get("Type 2"))
        
        return types

    @cached_property
    def types(self) -> list[str]:
        """
        Get types attribute
        """
        return self.get_types()


    def get_hp(self) -> int:
        return self._data.get("HP")

    @cached_property
    def hp(self) -> int:
        """
        Get hp attribute
        """
        return self.get_hp()


    def get_attack(self) -> int:
        return self._data.get("Attack")

    @cached_property
    def attack(self) -> int:
        """
        Get attack attribute
        """
        return self.get_attack()


    def get_defense(self) -> int:
        return self._data.get("Defense")

    @cached_property
    def defense(self) -> int:
        """
        Get defense attribute
        """
        return self.get_defense()


    def get_special_atk(self) -> int:
        return self._data.get("Special_Atk")

    @cached_property
    def special_atk(self) -> int:
        """
        Get special_atk attribute
        """
        return self.get_special_atk()


    def get_special_def(self) -> int:
        return self._data.get("Special_Def")

    @cached_property
    def special_def(self) -> int:
        """
        Get special_def attribute
        """
        return self.get_special_def()


    def get_special_def(self) -> int:
        return self._data.get("Special_Def")

    @cached_property
    def special_def(self) -> int:
        """
        Get special_def attribute
        """
        return self.get_special_def()


    def get_speed(self) -> int:
        return self._data.get("Speed")

    @cached_property
    def speed(self) -> int:
        """
        Get speed attribute
        """
        return self.get_speed()


    def get_generation_number(self) -> int:
        return self._data.get("Generation")

    @cached_property
    def generation_number(self) -> int:
        """
        Get generation_number attribute
        """
        return self.get_generation_number()


    def get_region(self) -> str:
        generation = self._data.get("Generation")
        return MAPPING_GENERATION_REGION.get(str(generation))

    @cached_property
    def region(self) -> str:
        """
        Get region attribute
        """
        return self.get_region()


    def get_legendary(self) -> bool:
        return self._data.get("Legendary")

    @cached_property
    def legendary(self) -> bool:
        """
        Get legendary attribute
        """
        return self.get_legendary()
