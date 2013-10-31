# predict what user (id=3) would rate Toy Story (1995)

# get Toy Story from the table Movies
m = session.query(Movie).filter_by(title="Toy Story (1995)").one()

# user with id=3 has not yet rated "toy story"
u = session.query(User).get(3) 

# get all RATINGS on Toy Story
other_ratings = session.query(Rating).filter_by(movie_id=m.id).all()

# get all USERS who had rated Toy Story
other_users = []
for r in other_ratings:
    other_users.append(r.user)
o = other_users[0]
paired_ratings = []
# create a pair list with the ratings from these 2 different users on movies
for r1 in u.ratings:
    for r2 in o.ratings:
        if r1.movie_id == r2.movie_id:
            paired_ratings.append( (r1.rating, r2.ratings) )
# OR user dictionary to speed up the creation
u_ratings = {}
for r in u.ratings:
    u_ratings[ r.movie_id ] = r
paired_ratings = []
for o_rating in o.ratings:
    u_rating = u_ratings.get(o_rating.movie_id)
    if u_rating:
        pair = (u_rating.rating, o_rating.rating)
        paired_ratings.append(pair)
