from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash, make_response, render_template_string
import json
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
from threading import Timer
import os
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from app import analytics


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

# vehicle endpoint
@app.route("/vehicle")
def vehicle_page():
    return render_template('vehicle.html')

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

# json query vehicle endpoint
@app.route("/query/new_query_vehicle")
def new_query_pull_vehicle():
    try:
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")
            
        # handle http get request arguments
        car_id = request.args.get('car_id')
        manu = request.args.get('manu')

        # return all rows from the pricing tables
        query = '''
                        SELECT {0}_pricing.*, manufacturers.manufacturer, transmissions.transmission_type, drivetrains.drivetrain_type FROM {0}_pricing JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id WHERE car_id = {1};
        '''.format(manu, car_id)
        # make db query
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close() 
        query_html = query_df.to_json()
        save_path = '/usr/src/api/app/templates'
        file_name = "new_query_vehicle.json"
        complete_name = os.path.join(save_path,file_name)
        with open(complete_name,"w") as f:
            f.write(query_html)
        f.close()
        return render_template("new_query_vehicle.json",data = query_df, index = False)
    except:
        return "render failed"

@app.route("/analytics")
def analytics_page():
    return render_template('open_analytics.html')

@app.route("/analytics_result", methods=['POST','GET'])
def analytics_build():
    try:
        manu1 = request.args.get('manu1')
        manu2 = request.args.get('manu2')
        drivetrain = request.args.get('drivetrain')
        transmission = request.args.get('transmission')

        msrp = bool(request.args.get('msrp'))
        fuel_tank_size = bool(request.args.get('fuel_tank_size'))
        mpg = bool(request.args.get('mpg'))
        horsepower = bool(request.args.get('horsepower'))
        try:
            db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
            print("successful connection")
        except:
            print("could not connect")
        query = analytics.manu_pull(manu1=manu1,manu2=manu2)
        query_df = pd.read_sql_query(query,con=db_conn)
        db_conn.close()
        query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
        query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
        query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
        query_df.rename(columns={"msrp_price":"Average_Msrp_Price","city_mpg":"Average_City_MPG","highway_mpg":"Average_Highway_MPG","fuel_tank_size":"Average_Fuel_Tank_Size","horsepower":"Average_Horsepower"}, inplace=True)
        df_html=query_df.to_html()
        if (drivetrain is not None and transmission is not None):
            if(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                #graphJSON2=graphJSON2,graphJSON3=graphJSON3
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                #fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                #graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.full_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
        elif(drivetrain is not None and transmission is None):
            if(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                #graphJSON2=graphJSON2,graphJSON3=graphJSON3
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                #fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                #graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.drive_pull(manu1=manu1,manu2=manu2,drivetrain=drivetrain)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
        elif(drivetrain is None and transmission is None):
            if(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                #graphJSON2=graphJSON2,graphJSON3=graphJSON3
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                #fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                #graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.manu_pull(manu1=manu1,manu2=manu2)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
        elif(drivetrain is None and transmission is not None):
            if(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                #graphJSON2=graphJSON2,graphJSON3=graphJSON3
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                #fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                #graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                #fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                #graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                #fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                #graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                #fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                #graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                #fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                #graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is False and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is True and fuel_tank_size is True and mpg is False and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig1 = px.bar(query_df,x="model",y="msrp_price",width=800,height=400)
                graphJSON = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON=graphJSON,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is True and horsepower is False):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON5=graphJSON5,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is False and mpg is True and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig2 = px.bar(query_df,x="model",y="city_mpg",width=800,height=400)
                graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
                fig3 = px.bar(query_df,x="model",y="highway_mpg",width=800,height=400)
                graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,df_html=df_html)
            elif(manu1 is not None and manu2 is not None and msrp is False and fuel_tank_size is True and mpg is False and horsepower is True):
                try:
                    db_conn = psycopg2.connect(host=host,port=port,user=user,password=password,dbname=dbname)
                    print("successful connection")
                except:
                    print("could not connect")
                query = analytics.transmission_pull(manu1=manu1,manu2=manu2,transmission=transmission)
                query_df = pd.read_sql_query(query,con=db_conn)
                db_conn.close()
                query_df["msrp_price"] = pd.to_numeric(query_df["msrp_price"])
                query_df["fuel_tank_size"] = pd.to_numeric(query_df["fuel_tank_size"])
                query_df=query_df.groupby(["manufacturer","model"], as_index=False)[["msrp_price","city_mpg","highway_mpg","horsepower","fuel_tank_size"]].mean().round(2)
                fig4 = px.bar(query_df,x="model",y="horsepower",width=800,height=400)
                graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
                fig5 = px.bar(query_df,x="model",y="fuel_tank_size",width=800,height=400)
                graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("analytics.html",graphJSON4=graphJSON4,graphJSON5=graphJSON5,df_html=df_html)
    except:
        return render_template("failed_analytics.html")

# healthcheck / ping endpoint
@app.route("/ping")
def ping():
    return {"result": "success!"}