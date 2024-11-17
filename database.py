from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL bazaga ulanish
DATABASE_URL = "mysql+pymysql://{user}:{password}@{host}:{port}/{name}".format(
    user='tmsitiuz',
    password='pwd4catalogDB',
    host='localhost',
    port='3306',
    name='tmsitiuz_catalog'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Ma'lumotlar bazasidan sessiya yaratish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
