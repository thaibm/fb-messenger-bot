# from database import db, Book
# import csv
#
# class Seed:
#     def __init__(self):
#         db.create_all()
#
#     def make(self):
#         with open("data/tiki-full.csv", "r", encoding="utf8") as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 book = Book(row['name'], row['author'], row["categories"], row["url"], row["description"])
#                 db.session.add(book)
#                 db.session.commit()
