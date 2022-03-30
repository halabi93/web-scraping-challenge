from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/scraping_app")


@app.route('/')
def index():
    scraping = mongo.db.scraping.find_one()
    return render_template('index.html', scraping = scraping)


@app.route('/scrape')
def scrape():
    scraping = mongo.db.scraping
    data = scrape_mars.scrape()
    scraping.update_one( {}, {"$set": data}, upsert = True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
