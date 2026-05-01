from sqlmodel import create_engine, Session
from models import SQLModel
import urllib.parse

password = urllib.parse.quote_plus("Qwer4126@tf2787")


DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/media_api"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session