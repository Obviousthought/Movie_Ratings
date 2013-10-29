from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    occupation = Column(String(64), nullable=True)
    zipcode = Column(String(15), nullable=True)
    


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=True)
    released_at = Column(Date(), nullable=True)
    imdb_url = Column(String(100), nullable=True)



class Data(Base):

    __tablename__ = "data"

    user_id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True)
    timestamp = Column(Integer, nullable=True) #Parse with Epoch/datetime later


### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    # Base.metadata.create_all(engine)
    pass

if __name__ == "__main__":
    main()
