from sqlalchemy import create_engine
from config import DB_URL

engine = create_engine(DB_URL, convert_unicode=True, pool_size=20, max_overflow=0)

