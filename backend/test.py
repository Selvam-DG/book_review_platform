from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

password = 'Selvam@557'
encoded_password = quote_plus(password)  # -> 'my%40Password%23123'


password = "Selvam@557"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://selvamdg:{encoded_password}@localhost:5432/Book_reviews"
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return jsonify([{'id': b.id, 'title': b.title} for b in all_books])

if __name__ == "__main__":
    app.run(debug=True)
