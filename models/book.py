from database import db, Book


class BookRecord:
    @staticmethod
    def get(book_id):
        book = db.session.query(Book).filter(Book.id == book_id).first()
        return book
    @staticmethod
    def get_by_name(name):
        _name = []
        for e in name.split():
            _name.append(e.capitalize())
        name = " ".join(_name)
        book = db.session.query(Book).filter(Book.name.like('%'+name+'%')).first()
        return book