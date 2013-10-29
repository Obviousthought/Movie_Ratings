import model
import csv
import datetime

def load_user(session):
    with open('seed_data/u.user', 'rb') as csvfile:
        user_db = csv.reader(csvfile, delimiter = '|')
        for row in user_db:
            new_user = model.User(id=row[0], age=row[1], gender=row[2], occupation=row[3], zipcode=row[4])
            session.add(new_user)
    session.commit()
    


def load_item(session):
    with open('seed_data/u.item', 'rb') as csvfile:
        item_db = csv.reader(csvfile, delimiter = '|')
        for row in item_db:
            date_release = row[2]
            date_release.datetime.datetime.strptime('%d-%b-%Y')
            title = row[1].decode("latin-1")
            new_movie = model.Item(id=row[0], name=title, released_at=date_release , imdb_url=row[3])
            session.add(new_movie)
    session.commit()
    


def load_data(session):
    with open('seed_data/u.data', 'rb') as csvfile:
        data_db = csv.reader(csvfile, delimiter = ' ')
        for row in data_db:
            new_user = model.Data(user_id=row[0], age=row[1], gender=row[2], occupation=row[3], zipcode=row[4])
            session.add(new_user)
    session.commit()
    

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_user(session)
    load_item(session)
    # load_data(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
