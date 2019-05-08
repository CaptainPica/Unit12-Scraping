from scrape_mars import scrape
import pymongo
from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db
col = db.mars_elements

@app.route("/")
def home():
    #Renders the most current record to the index.html
    records = list(db.col.find())
    record = records[len(records)-1]
    return render_template("index.html",record = record)

@app.route("/scrape")
def scrapy():
    #Adds a new record if it is at all different from any of the records already contained
    dic = scrape()
    db.col.replace_one(dic,dic,upsert=True)
    return redirect(location = url_for("home"), code=302)

if __name__ == "__main__":
    app.run(debug=True)
