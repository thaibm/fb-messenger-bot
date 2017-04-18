from database import db, Book


class BookRecord:
    @staticmethod
    def get(book_id):
        book = db.session.query(Book).filter(Book.id == book_id).first()
        return book
