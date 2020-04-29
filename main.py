from flask import Flask, request, render_template


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Air

app = Flask(__name__)


#Connect to Database and create database session
engine = create_engine('sqlite:///air-data.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bme680')
def bme680():
	air_data = session.query(Air).all()
	return render_template('bme680.html', air_data=air_data)


# #This will let us Create a new book and save it in our database
# @app.route('/books/new/',methods=['GET','POST'])
# def newBook():
#    if request.method == 'POST':
#        newBook = Book(title = request.form['name'], author = request.form['author'], genre = request.form['genre'])
#        session.add(newBook)
#        session.commit()
#        return redirect(url_for('showBooks'))
#    else:
#        return render_template('newBook.html')


# #This will let us Update our books and save it in our database
# @app.route("/books/<int:book_id>/edit/", methods = ['GET', 'POST'])
# def editBook(book_id):
#    editedBook = session.query(Book).filter_by(id=book_id).one()
#    if request.method == 'POST':
#        if request.form['name']:
#            editedBook.title = request.form['name']
#            return redirect(url_for('showBooks'))
#    else:
#        return render_template('editBook.html', book = editedBook)

# #This will let us Delete our book
# @app.route('/books/<int:book_id>/delete/', methods = ['GET','POST'])
# def deleteBook(book_id):
#    bookToDelete = session.query(Book).filter_by(id=book_id).one()
#    if request.method == 'POST':
#        session.delete(bookToDelete)
#        session.commit()
#        return redirect(url_for('showBooks', book_id=book_id))
#    else:
#        return render_template('deleteBook.html',book = bookToDelete)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')