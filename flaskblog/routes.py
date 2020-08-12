from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import pymongo
from pymongo import MongoClient
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been successfully created for {form.username.data}. Try Loggin in Now!','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful! Please check email and password')
  
    return render_template('login.html',title = 'Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/database")
@login_required
def database():
    # Connecting to Mongo DB
    cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/datasets?retryWrites=true&w=majority")
    db = cluster["datasets"]
    collection = db["insurance"]
    ans = list(collection.find({}))

    return render_template('database.html', ans=ans)


@app.route("/loaddb")
@login_required
def loaddb():
    # Converting CSV file to pandas dataframe
    df = pd.read_csv('dataset.csv')

    # Connecting to Mongo DB
    cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/datasets?retryWrites=true&w=majority")
    db = cluster["datasets"]
    collection = db["insurance"]

    # Converting dataframe to dictionary and adding '_id'
    dic = df.to_dict('records')
    for i in range(0,len(dic)):
        dic[i]['_id'] = i

    # Pushing dictionary to Mongo DB
    collection.insert_many(dic)

    ans = list(collection.find({}))

    return render_template('database.html', ans=ans)


@app.route("/deletedb")
@login_required
def deletedb():
    # Connecting to Mongo DB
    cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/datasets?retryWrites=true&w=majority")
    db = cluster["datasets"]
    collection = db["insurance"]
    collection.delete_many({})

    ans = list(collection.find({}))

    return render_template('database.html', ans=ans)


@app.route("/mlinfo")
def mlinfo():

    return render_template('mlinfo.html')


@app.route("/applyml")
@login_required
def applyml():

    try:

        cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/datasets?retryWrites=true&w=majority")
        db = cluster["datasets"]
        collection = db["insurance"]

        res = list(collection.find({}))
        cdf = pd.DataFrame(res)
        df = cdf[['smoker','age','bmi','children','sex','charges']]

        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values

        le = LabelEncoder()
        X[:,0] = le.fit_transform(X[:,0])
        X[:,4] = le.fit_transform(X[:,4])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        
        # Applying Multiple Regression
        from sklearn.linear_model import LinearRegression
        regressor_mlpr = LinearRegression()
        regressor_mlpr.fit(X_train, y_train)

        y_pred_mplr = regressor_mlpr.predict(X_test)
        np.set_printoptions(precision=2)
        result_mplr = np.concatenate((y_pred_mplr.reshape(len(y_pred_mplr),1), y_test.reshape(len(y_test),1)),1)
        ls_mplr = list(result_mplr[0:10,:])

        r2_mlrp = r2_score(y_test, y_pred_mplr)

        # Applying Decision Tree Regresssion
        from sklearn.tree import DecisionTreeRegressor
        regressor_dt = DecisionTreeRegressor(random_state = 0)
        regressor_dt.fit(X_train, y_train)

        y_pred_dt = regressor_dt.predict(X_test)
        result_dt = np.concatenate((y_pred_dt.reshape(len(y_pred_dt),1), y_test.reshape(len(y_test),1)),1)
        ls_dt = list(result_dt[0:10,:])

        r2_dt = r2_score(y_test, y_pred_dt)

        # Applying Random Forest Regression
        from sklearn.ensemble import RandomForestRegressor
        regressor_rf = RandomForestRegressor(n_estimators = 10, random_state = 0)
        regressor_rf.fit(X_train, y_train)

        y_pred_rf = regressor_rf.predict(X_test)
        result_rf = np.concatenate((y_pred_rf.reshape(len(y_pred_rf),1), y_test.reshape(len(y_test),1)),1)
        ls_rf = list(result_rf[0:10,:])

        r2_rf = r2_score(y_test, y_pred_rf)

        return render_template('applyml.html',ls_mplr=ls_mplr,r2_mlrp=r2_mlrp,ls_dt=ls_dt,r2_dt=r2_dt,ls_rf=ls_rf,r2_rf=r2_rf)

    except:

        return render_template('nodata.html')