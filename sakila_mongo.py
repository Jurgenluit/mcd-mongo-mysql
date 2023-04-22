import pymongo
from faker import Faker
import random
from bson.objectid import ObjectId

fake = Faker()

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://%s:%s@localhost:27017/"% ("root", "example"))
db = client["sakila"]

# Definición de colecciones
actor_col = db["actor"]
film_actor_col = db["film_actor"]
film_col = db["film"]
language_col = db["language"]
film_category_col = db["film_category"]
category_col = db["category"]

# Crear y llenar la colección 'language'
languages = ['English', 'Spanish', 'French', 'German', 'Italian', 'Japanese', 'Chinese', 'Russian']
language_ids = []
for lang in languages:
    language_doc = {"name": lang}
    result = language_col.insert_one(language_doc)
    language_ids.append(result.inserted_id)

# Crear y llenar la colección 'category'
categories = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Documentary']
category_ids = []
for cat in categories:
    category_doc = {"name": cat}
    result = category_col.insert_one(category_doc)
    category_ids.append(result.inserted_id)

# Crear y llenar la colección 'actor'
actor_ids = []
for _ in range(100):
    actor_doc = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    result = actor_col.insert_one(actor_doc)
    actor_ids.append(result.inserted_id)

# Crear y llenar la colección 'film'
film_ids = []
for _ in range(1000):
    film_doc = {
        "title": fake.sentence(nb_words=3),
        "description": fake.text(),
        "release_year": fake.year(),
        "language_id": random.choice(language_ids),
        "length": random.randint(80, 180),
        "rating": random.choice(['G', 'PG', 'PG-13', 'R', 'NC-17']),
    }
    result = film_col.insert_one(film_doc)
    film_ids.append(result.inserted_id)

# Crear y llenar la colección 'film_actor'
for film_id in film_ids:
    actors_in_film = random.sample(actor_ids, random.randint(1, 10))
    for actor_id in actors_in_film:
        film_actor_doc = {
            "actor_id": actor_id,
            "film_id": film_id,
        }
        film_actor_col.insert_one(film_actor_doc)

# Crear y llenar la colección 'film_category'
for film_id in film_ids:
    film_category_doc = {
        "film_id": film_id,
        "category_id": random.choice(category_ids),
    }
    film_category_col.insert_one(film_category_doc)

print("Datos generados e insertados con éxito.")
