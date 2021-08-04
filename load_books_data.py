from model import *
from app import app,db
import csv



def main():
    data=open('books.csv')
    read=csv.reader(data)
    
    for i in read:
        row=Books(isbn=i[0],title=i[1],author=i[2],year=i[3])
        db.session.add(row)
    db.session.commit()

if __name__=='__main__':
    with app.app_context() :
        main()

