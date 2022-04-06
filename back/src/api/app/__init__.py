from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import json
import requests
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
from threading import Timer
import os

# db vars
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
dbname = os.environ.get("DB_NAME")

app = Flask(__name__, static_folder='static') # static folder for stylesheets, scripts, etc
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.permanent_session_lifetime = timedelta(hours=12)

## testing endpoints ##
# site home endpoint
@app.route("/")
def home_page():
    return render_template('home.html')

# cards endpoint
@app.route("/cards")
def card_page():
    return render_template('cards.html')

# search endpoint
@app.route("/search")
def search_page():
    return render_template('search.html')

# site favorites endpoint
@app.route("/favorites")
def favorites_page():
    return render_template('favorites.html')

# about endpoint
@app.route("/about")
def about_page():
    return render_template('about.html')

# featured endpoint
@app.route("/featured")
def featured_page():
    return render_template('featured.html')

# json query endpoint
@app.route("/query/json")
def json_query_pull():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")

        # handle http get request arguments
        manu = request.args.get('manu')
        model = request.args.get('model')
            
        price_min = request.args.get('price_min')
        price_max = request.args.get('price_max')

        hp_min = request.args.get('hp_min')
        hp_max = request.args.get('hp_max')

        mpg_min = request.args.get('mpg_min')
        mpg_max = request.args.get('mpg_max')

        # form query string based on input value
        query = '''
            SELECT {0}_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type 
            FROM {0}_pricing 
            JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id 
            WHERE model LIKE '%{1}%' 
            AND CAST(msrp_price AS INTEGER) BETWEEN {2} AND {3}
            AND horsepower BETWEEN {4} AND {5}
            AND city_mpg BETWEEN {6} AND {7};
        '''.format(manu, model, price_min, price_max, hp_min, hp_max, mpg_min, mpg_max)
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query.json",data = query_df, index = False)
    except:
        return "render failed"

# json query models endpoint
@app.route("/query/models_json")
def json_query_pull_models():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")

        # handle http get request arguments
        manu = request.args.get('manu')
            
        # form query string based on input value
        query = "SELECT DISTINCT model FROM {0}_pricing;".format(manu)
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query_models.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query_models.json",data = query_df, index = False)
    except:
        return "render failed"

# json query all endpoint
@app.route("/query/all_json")
def json_query_pull_all():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")
            
        # handle http get request arguments
        price_min = request.args.get('price_min')
        price_max = request.args.get('price_max')

        hp_min = request.args.get('hp_min')
        hp_max = request.args.get('hp_max')

        mpg_min = request.args.get('mpg_min')
        mpg_max = request.args.get('mpg_max')

        # return all rows from the pricing tables
        query = '''
            SELECT toyota_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM toyota_pricing JOIN manufacturers ON toyota_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON toyota_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON toyota_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5}
            UNION SELECT ford_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM ford_pricing JOIN manufacturers ON ford_pricing.manufacturer_id = manufacturers.manufacturer_id  JOIN transmissions ON ford_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON ford_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5}
            UNION SELECT lamborghini_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM lamborghini_pricing JOIN manufacturers ON lamborghini_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON lamborghini_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON lamborghini_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5}
            UNION SELECT subaru_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM subaru_pricing JOIN manufacturers ON subaru_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON subaru_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON subaru_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5}
            UNION SELECT honda_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM honda_pricing JOIN manufacturers ON honda_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON honda_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON honda_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5}
            UNION SELECT bmw_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM bmw_pricing JOIN manufacturers ON bmw_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON bmw_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON bmw_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5}
            UNION SELECT ferrari_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM ferrari_pricing JOIN manufacturers ON ferrari_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON ferrari_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON ferrari_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE CAST(msrp_price AS INTEGER) BETWEEN {0} AND {1} AND horsepower BETWEEN {2} AND {3} AND city_mpg BETWEEN {4} AND {5};
        '''.format(price_min, price_max, hp_min, hp_max, mpg_min, mpg_max)
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query_all.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query_all.json",data = query_df, index = False)
    except:
        return "render failed"

# json query simple endpoint
@app.route("/query/json_simple")
def json_query_pull_simple():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")

        # handle http get request arguments
        manu = request.args.get('manu')

        # form query string based on input value
        query = '''
            SELECT {0}_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type 
            FROM {0}_pricing 
            JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id;
        '''.format(manu)
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query.json",data = query_df, index = False)
    except:
        return "render failed"

# json query random endpoint
@app.route("/query/random_json")
def json_query_pull_random():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")
        # return 10 rows randomly from all pricing tables
        query = '''
            SELECT * FROM (
                (SELECT toyota_pricing.*, manufacturers.manufacturer FROM toyota_pricing
                JOIN manufacturers ON toyota_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
                UNION ALL
                (SELECT ford_pricing.*, manufacturers.manufacturer FROM ford_pricing
                JOIN manufacturers ON ford_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
                UNION ALL
                (SELECT lamborghini_pricing.*, manufacturers.manufacturer FROM lamborghini_pricing
                JOIN manufacturers ON lamborghini_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
                UNION ALL
                (SELECT subaru_pricing.*, manufacturers.manufacturer FROM subaru_pricing
                JOIN manufacturers ON subaru_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
                UNION ALL
                (SELECT honda_pricing.*, manufacturers.manufacturer FROM honda_pricing
                JOIN manufacturers ON honda_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
                UNION ALL
                (SELECT bmw_pricing.*, manufacturers.manufacturer FROM bmw_pricing
                JOIN manufacturers ON bmw_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
                UNION ALL
                (SELECT ferrari_pricing.*, manufacturers.manufacturer FROM ferrari_pricing
                JOIN manufacturers ON ferrari_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 10)
            ) AS TOP
            ORDER BY RANDOM();
        '''
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query_random.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query_random.json",data = query_df, index = False)
    except:
        return "render failed"

# json query one random endpoint
@app.route("/query/one_random_json")
def json_query_pull_one_random():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")

        x=datetime.today()
        y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
        delta_t=y-x

        secs=delta_t.seconds+1

        query = '''
            SELECT * FROM (
                (SELECT toyota_pricing.*, manufacturers.manufacturer FROM toyota_pricing
                JOIN manufacturers ON toyota_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
                UNION ALL
                (SELECT ford_pricing.*, manufacturers.manufacturer FROM ford_pricing
                JOIN manufacturers ON ford_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
                UNION ALL
                (SELECT lamborghini_pricing.*, manufacturers.manufacturer FROM lamborghini_pricing
                JOIN manufacturers ON lamborghini_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
                UNION ALL
                (SELECT subaru_pricing.*, manufacturers.manufacturer FROM subaru_pricing
                JOIN manufacturers ON subaru_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
                UNION ALL
                (SELECT honda_pricing.*, manufacturers.manufacturer FROM honda_pricing
                JOIN manufacturers ON honda_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
                UNION ALL
                (SELECT bmw_pricing.*, manufacturers.manufacturer FROM bmw_pricing
                JOIN manufacturers ON bmw_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
                UNION ALL
                (SELECT ferrari_pricing.*, manufacturers.manufacturer FROM ferrari_pricing
                JOIN manufacturers ON ferrari_pricing.manufacturer_id = manufacturers.manufacturer_id ORDER BY RANDOM() LIMIT 1)
            ) AS TOP
            ORDER BY RANDOM()
            LIMIT 1;
        '''
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query_one_random.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query_one_random.json",data = query_df, index = False)
        t = Timer(secs, one_random)
        t.start()
    except:
        return "render failed"

# healthcheck / ping endpoint
@app.route("/ping")
def ping():
    return {"result": "success!"}
