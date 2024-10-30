POKEMON_SCHEMA = [
    {"name": "pokemon_name", "type": "STRING", "mode": "REQUIRED"},
    {"name": "types", "type": "STRING", "mode": "REPEATED"},
    {"name": "hp", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "attack", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "defense", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "special_atk", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "special_def", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "speed", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "generation_number", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "region", "type": "STRING", "mode": "NULLABLE"},
    {"name": "legendary", "type": "BOOLEAN", "mode": "NULLABLE"},
]
