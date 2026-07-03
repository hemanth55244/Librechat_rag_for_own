# app/utils/health.py
from app.config import VECTOR_DB_TYPE, VectorDBType


async def is_health_ok():
    if VECTOR_DB_TYPE == VectorDBType.PGVECTOR:
        from app.services.database import pg_health_check

        return await pg_health_check()
    if VECTOR_DB_TYPE == VectorDBType.ATLAS_MONGO:
        from app.services.mongo_client import mongo_health_check

        return await mongo_health_check()
    else:
        return True
