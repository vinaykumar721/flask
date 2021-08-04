from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()



class User(db. Model):
    __tablename__="User"

    username=db.Column(db.String(80),primary_key=True,nullable=False)
    email=db.Column(db.String(80),nullable=False)
    password=db.Column(db.String(80),nullable=False)
    timestamp=db.Column(db.String(80),nullable=False)


class Books(db.Model):

    __tablename__="Books"

    isbn=db.Column(db.String(80),primary_key=True, nullable=False)
    title = db.Column(db.String(500), unique=False, nullable=False)
    author = db.Column(db.String(500), unique=False, nullable=False)
    year = db.Column(db.String(80), unique=False, nullable=False)




class Review(db.Model):
    __tablename__ = "Review"
    isbn = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)



class Shelf(db.Model):
    __tablename__="Shelf"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False)
    author = db.Column(db.String, unique=False, nullable=False)
    year = db.Column(db.String, unique=False, nullable=False)
    name=db.Column(db.String(80),primary_key=True,nullable=False)
    




