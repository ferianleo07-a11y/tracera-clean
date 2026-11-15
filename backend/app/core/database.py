import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.app.core.config import settings

logger = logging.getLogger("uvicorn.info")

class MongoDBManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db_manager = MongoDBManager()

async def connect_to_database():
    """Inisialisasi connection pool MongoDB saat server FastAPI startup."""
    try:
        logger.info(f"[*] Menghubungkan ke MongoDB Atlas: {settings.DB_NAME}...")
        db_manager.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000
        )
        db_manager.db = db_manager.client[settings.DB_NAME]
        # Ping server untuk memverifikasi koneksi aktif
        await db_manager.client.admin.command('ping')
        logger.info("[OK] Sukses terhubung ke cluster MongoDB Atlas!")
    except Exception as e:
        logger.error(f"[!] Gagal menghubungkan ke MongoDB: {e}")
        raise e

async def close_database_connection():
    """Menutup pool koneksi MongoDB saat server FastAPI shutdown."""
    if db_manager.client:
        logger.info("[*] Menutup koneksi MongoDB Atlas...")
        db_manager.client.close()
        logger.info("[OK] Pool koneksi MongoDB berhasil ditutup.")

async def get_database() -> AsyncIOMotorDatabase:
    """FastAPI Dependency untuk menginjeksi instance database ke dalam route handlers."""
    if db_manager.db is None:
        raise RuntimeError("Database belum terhubung! Pastikan startup lifespan berjalan.")
    return db_manager.db