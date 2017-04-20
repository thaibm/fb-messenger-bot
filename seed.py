from database import db, Book
import csv

class Seed:
    def __init__(self):
        db.create_all()

    def make(self):
        with open('data/tiki-full.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row[2].strip())
                book = Book(row[2], row[4], row[3], row[0], row[1])
                db.session.add(book)
                db.session.commit()
