from flask import render_template, url_for, flash, redirect
from flaskblog import app
import pandas as pd
import pymongo
from pymongo import MongoClient


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/database")
def database():
    # Connecting to Mongo DB
    cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["test"]
    collection = db["test"]
    ans = list(collection.find({}))

    return render_template('database.html', ans=ans)

@app.route("/loaddb")
def loaddb():
    # Converting CSV file to pandas dataframe
    df = pd.read_csv('vgdata.csv')

    # Connecting to Mongo DB
    cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["test"]
    collection = db["test"]

    # Converting dataframe to dictionary and adding '_id'
    dic = df.to_dict('records')
    for i in range(0,len(dic)):
        dic[i]['_id'] = i

    # Pushing dictionary to Mongo DB
    collection.insert_many(dic)

    ans = list(collection.find({}))

    return render_template('database.html', ans=ans)

@app.route("/deletedb")
def deletedb():
    # Connecting to Mongo DB
    cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["test"]
    collection = db["test"]
    collection.delete_many({})

    ans = list(collection.find({}))

    return render_template('database.html', ans=ans)