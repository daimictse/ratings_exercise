import model
import csv
import datetime

def load_users(session):
    # use u.user
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            user = model.User(id=row[0], age=row[1], zipcode=row[4])
            session.add(user)
            
    session.commit()

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if (row[2]):
                released_date = datetime.datetime.strptime(row[2], "%d-%b-%Y")
            else:
                released_date = None
            movie_name = row[1]
            movie_name = movie_name.decode("latin-1")
            movie = model.Movies(id=row[0], name=movie_name, released_at=released_date, imdb_url=row[4])
            session.add(movie)

    session.commit()


def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            rating = model.Ratings(user_id=row[0], movie_id=row[1], rating=row[2])
            session.add(rating)
            
    session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(s)
    load_ratings(s)
    load_movies(s)

if __name__ == "__main__":
    s= model.connect()
    main(s)
