from database import db, Book
import csv

class Seed:
    def __init__(self):
        db.create_all()

    def make(self):
        with open('data/test.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print (row['name'], row['author'])
                book = Book(row['name'], row['author'], row['categories'], row['url'], row['description'])
                db.session.add(book)
                db.session.commit()
