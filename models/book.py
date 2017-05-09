from database import db, Book


class BookRecord:
    @staticmethod
    def get(book_id):
        book = db.session.query(Book).filter(Book.id == book_id).first()
        return book
    @staticmethod
    def get_by_name(name):
        name = name.lower()
        book = db.session.query(Book).filter(Book.name.like('%'+name+'%')).first()