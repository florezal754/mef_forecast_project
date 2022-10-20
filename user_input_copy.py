#import flask library making code available to the rest of the app
from flask import Flask, request, jsonify, render_template
#flask provides with jsonify function to convert lists and dict to JSON 
from flask_cors import CORS

#creates the Flask app object, contains data about the app and methods (object functions)
#functions tell the app to do certain actions
app = Flask(__name__)
CORS(app)

#starts the debugger -- if code is malformed an error will appear
app.config["DEBUG"] = True

import json 
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px

#ask for int user input
@app.route('/user')
def ask_user():
    num = input('Enter a value:')
    print(num)

#conding the form in the flask file
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/data/', methods = ['POST','GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to 'form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html', form_data = form_data)


#co2 = pd.read_csv('co2.csv')
#ps = pd.read_csv('penalty_signals.csv')
import get_forecasted_data

df = pd.DataFrame(columns=["PBF_shortname","PBF_value", "PBF_datetime", "PBF_datetime_utc", "PBF_tz_time"])
values_df = get_forecasted_data.get_values(df)
datetime_df = get_forecasted_data.set_datetime_index(values_df)
sorted_df = get_forecasted_data.sort_pivot(datetime_df)
file = sorted_df.to_csv('frame.csv')
ps = pd.read_csv('frame.csv')
ps = ps.fillna(0)
df_plot = ps.drop(['PBF_datetime','Generación PBF total', 'Demanda Peninsular'], axis=1)
print('printing it',ps)

def my_plot(data,plot_var):
    data_plot = go.Scatter(x=ps.PBF_datetime,y=ps['Biomasa'], line=dict(color="#CE285E",width=2))
    layout=go.Layout(title=dict(text="This is a Line Chart",x=0.5), 
                     xaxis_title="datetime", yaxis_title="Plot_variables")
    fig =go.Figure(data=data_plot, layout=layout)

    #"This is a Line Chart of Variable"+" "+str(plot_var)
    
    # This is conversion step...
    fig_json = fig.to_json()
    graphJSON = json.dumps(fig_json, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def my_plot_full(dataframe):
    data_plot = px.line(df_plot,x=ps.PBF_datetime,y=df_plot.columns, title='forecasted data')
    fig_json = data_plot.to_json()
    graphJSON = json.dumps(fig_json, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def my_plot_full_bar(dataframe):
    data_plot = px.bar(df_plot,x=ps.PBF_datetime,y=df_plot.columns, title='forecasted data')
    fig_json = data_plot.to_json()
    graphJSON = json.dumps(fig_json, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

    
#def data_downloader():
    #to_display = (X=datetime == input.datetime) (Y=MEFmodel) 
    #data_download = ps.PBF_datetime_utc, ps.MEFmodel
    #return summmary, csv 


#pass the JSON object as the input of the render template function
@app.route('/', methods=['GET', 'POST'])
def home():
    #import chart as JSON object
    chart_from_python=my_plot(ps, ps.Biomasa)
    #pass the JSON Chart object into the frontend
    return render_template("sample_page.html", chart_for_html=chart_from_python)

@app.route('/full', methods=['GET', 'POST'])
def home_full():
    #import chart as JSON object
    chart_from_python=my_plot_full_bar(df_plot)
    #pass the JSON Chart object into the frontend
    return render_template("w3template.html", chart_for_html=chart_from_python)

@app.route('/about', methods=['GET'])
def about():
    return "<h1>XX</p>"


#method to do the action of run the app/ this runs the app server
app.run()