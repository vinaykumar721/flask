
from flask import Flask, render_template, request, redirect, url_for,session,jsonify
from datetime import datetime
from flask_session import Session
from model import *
from sqlalchemy import and_



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
url="postgresql://ohnxwmszghibsw:8747e0ae9cfe9b2aa3151bfa4eb8ed37de2f4f7e2e54c49b579a6769e7693ae0@ec2-35-168-198-9.compute-1.amazonaws.com:5432/d3rh39l8mf7hcn"
app.config["SQLALCHEMY_DATABASE_URI"] = url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def first():
    db.create_all()

with app.app_context():
    first()


@app.route("/")
def home():
    if 'username' in session:
        return render_template("searchbook.html")
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.pop('username',None)
    return render_template("home.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if(request.method=="POST"):
        email=request.form.get("email")
        password=request.form.get("password")
        users=User.query.all()
        print(email,password)
        print(users)

        for user in users:
            e=user.email
            pwd=user.password
            u=user.username
            print(e,pwd)
            if(email==e) and(password==pwd):
                session['username']=u
                print(u)
                return render_template("searchbook.html")
            
        error="Invalid username and password"
        return render_template("login.html",error=error)
    else:
        return render_template("login.html")
    # return redirect(url_for('hello'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method=="POST"):
        uname = request.form.get("uname")
        email = request.form.get("email")
        password = request.form.get("password")
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        time=datetime.now()
        users=User.query.all()
        
        for user in users:
            u=user.username
            e=user.email
            if(email==e) or (uname==u):
                d1="username or email is already Registered"
                d2="Please try Login."
                # print(d1)
                return render_template("register.html",error1=d1,error2=d2)  
                
        # print(uname,email,password)
        row=User(username=uname,email=email,password=password,timestamp=time)
        db.session.add(row)
        db.session.commit()

        return render_template("register.html",uname=uname)
    else:
        error="Invalid Username or password"
        return render_template("register.html",error=error)

@app.route('/admin')
def admin():
    return render_template("admin.html",users=User.query.all())

@app.route("/search",methods=["GET","POST"])
def search():
    # data=request.json
    if request.method=="GET" or "POST":
        s=request.form.get("search")
        # s=data["search"]
        print(s)

        usr_isbn=Books.query.filter(Books.isbn.ilike('%'+s+'%')).all()
        usr_title=Books.query.filter(Books.title.ilike('%'+s+'%')).all()
        usr_author=Books.query.filter(Books.author.ilike('%'+s+'%')).all()
        usr_year=Books.query.filter(Books.year.ilike('%'+s+'%')).all()
        print(usr_isbn)

        
        books=usr_isbn+usr_title+usr_author+usr_year
    # isbns=[]
    # titles=[]
    # authors=[]
    # years=[]
    # for i in books:
    #     isbns.append(i.isbn)
    #     titles.append(i.title)
    #     authors.append(i.author)
    #     years.append(i.year)
        
    # dict={
    #     "isbns":isbns,
    #     "titles":titles,
    #     "authors":authors,
    #     "years":years
    # }

    return render_template('searchbook.html',books=books)
    # return jsonify(dict),200

@app.route('/rr/<isbn>',methods=['GET',"POST"])
def get_book_details(isbn):
    a="rr.html"
    usr_isbn=Books.query.filter(Books.isbn==isbn).first()
    # print("Entered into rr")
    # if request.method=="POST":
    session['bookid'] = isbn
    
    r=Review.query.filter(Review.isbn==isbn)
    shelfbutton = True
    reviewbutton = True
    if 'username' in session:
        user = session['username']
        bookdetails = Books.query.filter(Books.isbn==isbn).first()
        if 'rsubmit' in request.form:
            s = Shelf(isbn=isbn,title = bookdetails.title, author=bookdetails.author,year = bookdetails.year, name=user)
            db.session.add(s)
            db.session.commit()
        elif 'delete' in request.form:
            Shelf.query.filter(Shelf.isbn== isbn,Shelf.name==user).delete()
            db.session.commit()

        try:
            a = Shelf.query.filter(Shelf.isbn==isbn).first()
            b = Review.query.filter(Review.isbn==isbn).first()
            if a!=None:
                shelfbutton = False
            else:
                shelfbutton = True
            if b!=None:
                reviewbutton = False
            else:
                reviewbutton = True
        except:
            pass

    return render_template("rr.html",book=usr_isbn,reviews=r,shelfbutton=shelfbutton,reviewbutton=reviewbutton)
    # else:
    #     print("Get")
    #     r=Review.query.filter(Review.isbn==isbn)
    #     return render_template("rr.html",book=usr_isbn,reviews=r,shelfbutton=True)


@app.route("/reviewrating",methods=['GET','POST'])
def reviewrating():
    if request.method == 'POST':
        print("review submitted")
        review=request.form.get("reviewdata")
        rating=request.form.get("ratingdata")
        name=session['username']
        print(name)
        print(rating)
        print(review)
        isbn = session['bookid']
        usr_isbn=Books.query.filter(Books.isbn==isbn).first()
        try:
            data=Review(isbn=isbn,name=name,review=review,rating=rating)
            db.session.add(data)
            db.session.commit()
            r=Review.query.filter(Review.isbn==isbn)
        except:
            r=Review.query.filter(Review.isbn==isbn)
            print(r)
        
        return render_template("rr.html",book=usr_isbn,reviews=r)

@app.route('/removefromshelf',methods=['GET','POST'])
def removefromshelf(isbn):
    usrname=session["username"]
    if 'delete' in  request.form:
        print("delete in removefromshelf")
        # n=request.form.get("name")
        # i=request.form.get("isbn")
        # t=request.form.get("title")
        # a=request.form.get("author")
        # y=request.form.get("year")
        # print(n,i,t,a,y)
        print(isbn)
        Shelf.query.filter(Shelf.isbn== isbn,Shelf.name==usrname).delete()
        db.session.commit()
    print(usrname)
    return render_template("bookshelf.html",users=Shelf.query.filter(Shelf.name==usrname).all())

@app.route('/bookshelf',methods=["GET","POST"])
def bookshelf():
    # sh=request.form.get("bookshelf")
    try:
        n=session["username"]
        print(n)
        if 'delete' in  request.form:
            n=request.form.get("name")
            i=request.form.get("isbn")
            t=request.form.get("title")
            a=request.form.get("author")
            y=request.form.get("year")
            print(n,i,t,a,y)
            print(n)
            Shelf.query.filter(Shelf.isbn== i,Shelf.name==n).delete()
            db.session.commit()

        return render_template("bookshelf.html",users=Shelf.query.filter(Shelf.name==n).all())
    except:
        return render_template("bookshelf.html",error="Already Logged out")
# @app.route('/bookdata/<isbn>',methods=['POST'])
# def shelf(isbn):
@app.route("/api/book", methods=["POST"])
def apiBook():
    data = request.json
    isbn = data["isbn"]
    bookObj = Books.query.filter_by(isbn=isbn).first()
    list = Review.query.filter_by(isbn=isbn).all()
    dict = {}
    if len(list) == 0:
        dict["users"] = ["-"]
        dict["ratings"] = [0]
        dict["reviews"] = ["-"]
        return jsonify(dict), 200
    users = []
    ratings = []
    reviews = []
    for i in list:
        users.append(i.name)
        ratings.append(i.rating)
        reviews.append(i.review)
    dict = {
        "users" : users,
        "ratings" : ratings,
        "reviews" : reviews
    }
    return jsonify(dict), 200

    
@app.route("/api/submit_review", methods=["POST"])
def apiSubmitReview():
  data = request.json
  user = data["user"]
  isbn = data["isbn"]
  rating = data["rating"]
  review = data["review"]
  obj = Review.query.filter(and_(Review.isbn == isbn, Review.name == user)).first()
  if obj is not None:
    return jsonify({"Message":"Already reviewed for this book"})
  else:
    reviewObj = Review(isbn=isbn, name=user, rating=rating, review=review)
    db.session.add(reviewObj)
    db.session.flush()
    db.session.commit()
    return jsonify({"Message":"Successfully Reviewed"})

@app.route('/addtoshelf',methods=['GET','POST'])
def addtoshelf():
    bookid = session['bookid']
    # print(bookid)
    bookdetails = Books.query.filter(Books.isbn==bookid).first()
    r=Review.query.filter(Review.isbn==bookid)
    print(r)
    shelfbutton = True
    if 'username' in session:
        user = session['username']
        try:
            s = Shelf(isbn=bookid,title = bookdetails.title, author=bookdetails.author,year = bookdetails.year, name=user)
            db.session.add(s)
            db.session.commit()
            print("try block in add to shelf")
            shelfbutton = False
        except:
            shelfbutton = False
    return render_template("rr.html",book=bookdetails,reviews=r,shelfbutton=shelfbutton)
    

