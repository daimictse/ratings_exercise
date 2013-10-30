from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy.orm import sessionmaker, scoped_session

ENGINE = None
Session = None

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column (String(15), nullable = True)

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = True)
    released_at = Column(Date(), nullable = True)
    imdb_url = Column(String(128), nullable = True)

class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movies", backref=backref("ratings", order_by=id))


### End class declarations

def authenticate(emailAddr, password):
    user = session.query(User).filter(User.email==emailAddr).filter(User.password==password).first()
    if (user):
        print user.id
        return user
    return None

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
