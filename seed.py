import model
import csv
import datetime

def load_user(session):
    with open('seed_data/u.user', 'rb') as csvfile:
        user_db = csv.reader(csvfile, delimiter = '|')
        for row in user_db:
            new_user = model.User(id=row[0], age=row[1], zipcode=row[4])
            session.add(new_user)
    session.commit()
    


def load_item(session):
    with open('seed_data/u.item', 'rb') as csvfile:
        item_db = csv.reader(csvfile, delimiter = '|')
        for row in item_db:

            title = row[1].decode("latin-1")

            release_date = row[2]
            if release_date != "":
                formatted_date = datetime.datetime.strptime(release_date, "%d-%b-%Y")

            else:
                pass
            new_movie = model.Movie(id=row[0], name=title, released_at=formatted_date , imdb_url=row[4])
            session.add(new_movie)
    session.commit()
    


def load_data(session):
    with open('seed_data/u.data', 'rb') as csvfile:
        data_db = csv.reader(csvfile, delimiter = '\t')
        for row in data_db:
            timestamp = int(row[3])
            formatted_timestamp = datetime.datetime.utcfromtimestamp(timestamp)
            new_data= model.Rating(user_id=row[0], movie_id=row[1], rating=row[2], timestamp=formatted_timestamp)
            session.add(new_data)
    session.commit()
    

def main():
    # You'll call each of the load_* functions with the session as an argument
    session = model.connect()
    load_user(session)
    print "user loaded"
    load_item(session)
    print "movies loaded"
    load_data(session)
    print "ratings loaded"

if __name__ == "__main__":
    s = model.connect()
    main(s)
