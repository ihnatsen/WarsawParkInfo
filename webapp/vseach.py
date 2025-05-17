from flask import Flask, render_template, request, send_from_directory
from database.postgres_database_connection import PostgresDatabaseConnection


app = Flask(__name__)

config = {
    'dbname': 'WarsawPark',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': 5432}


@app.route('/')
@app.route('/entry', methods=['GET', 'POST'])
def entry_page() -> 'html':
    return render_template('test_entry.html')


@app.route('/some_park')
def park_page() -> 'html':
    return render_template('test_some_park.html')


@app.route("/map")
def index():
    return render_template("index.html")


@app.route('/search', methods=['GET', 'POST'])
def search_page() -> 'html':
    with PostgresDatabaseConnection(**config) as db:
        district = str(request.form['district']) or None
        subway = str(request.form['subway']) or None
        rating = str(request.form['rating']) or None
        records = db.get_park_list(district=district, subway=subway, rating_category=rating)
        return render_template('test_some_park.html',
                               n=len(records),
                               parks=records
                               )


if __name__ == '__main__':
    app.run(debug=True)
