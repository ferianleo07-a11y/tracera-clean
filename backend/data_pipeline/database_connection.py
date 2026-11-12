import os
import json
from pymongo import MongoClient
from bson import json_util
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'tracera')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'raw_linkedin')

def connect_to_mongodb_and_get_data(uri, db_name, collection_name, query={}):
    """Menghubungkan ke MongoDB Atlas dan mengekstrak dokumen dalam format JSON mentah."""
    if not uri:
        raise ValueError("Kredensial MONGO_URI tidak ditemukan! Pastikan file .env sudah ada.")
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        documents = list(collection.find(query))
        json_data = json.loads(json_util.dumps(documents))
        print(f"Berhasil terhubung! {len(json_data)} dokumen dimuat dari koleksi '{collection_name}'.")
        return json_data
    except Exception as e:
        print(f"Error koneksi basis data: {e}")
        return []

raw_documents = connect_to_mongodb_and_get_data(MONGO_URI, DB_NAME, COLLECTION_NAME)
print(f"Sampel dokumen pertama: {json.dumps(raw_documents[0] if raw_documents else {}, indent=2)[:300]}...")