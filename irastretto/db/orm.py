""":mod:'irastretto.db.orm'

"""
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import declarative_base

Base = declarative_base()
Session = sessionmaker(autocommit=True)
