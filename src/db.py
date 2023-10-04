import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# postgresql://username:password@domain_name:port/database_name    - Так має виглядати URL
file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")    # Дістаємо файл config.ini, який лежить на два рівня вище
config = configparser.ConfigParser()   # Створюємо config. Допомагає нам читати файли .ini
config.read(file_config)      # Читаємо його

username = config.get("DB", "USER")   # Першою пишемо секцію - це DB, а потім що хочемо дістати
password = config.get("DB", "PASSWORD")
database_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")

url = f"postgresql://{username}:{password}@{domain}:5432/{database_name}"
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()
