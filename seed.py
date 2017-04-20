from database import db, Book
import csv

class Seed:
    def __init__(self):
        db.create_all()

    def make(self):
        with open('data/tiki.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row[2].strip())
                book = Book(row[2].strip(), row[4].strip(), row[3].strip(), row[0].strip(), row[1].strip())
                db.session.add(book)
                db.session.commit()
