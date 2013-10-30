from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref



ENGINE = None
Session = None
# session = Session()

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()
# session = sessionmaker(bind=ENGINE)


### Class declarations go here
class User(Base): #Users

    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    occupation = Column(String(64), nullable=True)
    zipcode = Column(String(15), nullable=True)
    


class Item(Base): #Movie

    __tablename__ = "items"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=False)
    released_at = Column(Date(), nullable=False)
    imdb_url = Column(String(100), nullable=False)

class Data(Base): #Rating

    __tablename__ = "data"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False) #Parse with Epoch/datetime later

    user = relationship("User", backref = backref("data", order_by = id))
    movie = relationship("Item", backref=backref("data", order_by=id))

### End class declarations


def main():
    """In case we need this for something"""
    pass

# def connect():
#     global ENGINE
#     global Session
#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)
#     return Session()

def initiate():
    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Base.metadata.create_all(ENGINE)

if __name__ == "__main__":
    # initiate()
    main()
