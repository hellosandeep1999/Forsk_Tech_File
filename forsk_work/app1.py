# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 21:12:50 2020

@author: user
"""

import flask                                               # pip install Flask
import pandas as pd                                        # pip install pandas
import dash                                                # pip install dash
import dash_core_components as dcc                          #pip install dash-core-components
import dash_html_components as html                         # pip install dash-html-components
from dash.dependencies import Input, State, Output           # pip install dash-renderer
import pandas as pd
import plotly.graph_objects as go                            #pip install plotly
import plotly.express as px
import dash_table as dt  
import dash_table
import webbrowser
from threading import Timer
import dash_bootstrap_components as dbc                     #pip install dash-bootstrap-components
import os
import math


#this line we use to hide some warnings which gives by pandas
pd.options.mode.chained_assignment = None


def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')


external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

list1 = ["Line","Bar"]


app.layout = html.Div(
        html.Div([
                


   html.Div(children=[
    
    #dropdown (Days)
    dbc.Container(
    html.Div([dcc.Dropdown(id='dd',
        options=[{'label': c , 'value': c} for c in list1],
        value=list1[0])],
    style={
            'width':'40%',
            'padding':40,
            'justify-content': 'center',
            'margin-left':220
        }
    ),
    ),

    dcc.Graph(id = 'graph'),
    
     
]),
    
])
)
    
    
    
    
@app.callback(dash.dependencies.Output('graph','figure'),[dash.dependencies.Input('dd','value')])

def update_fig(value):
    if value == 'Bar':
        data = [['mohan', 10], ['ramesh', 15], ['ganesh', 14],['divya', 20], ['rohan',25], ['sita', 18]]
        df = pd.DataFrame(data, columns = ['Name', 'Age']) 
        figure = px.bar(df, y ='Age',x = 'Name',
                        text='Age',
                        hover_data=['Name'],
                        height=500)
        
    if value == 'Line':
        data = [['mohan', 10], ['ramesh', 15], ['ganesh', 14],['divya', 20], ['rohan',25], ['sita', 18]]
        df = pd.DataFrame(data, columns = ['Name', 'Age']) 
        figure = go.Figure(data=go.Scatter(x=df['Name'], y=df['Age']))
        
    return figure


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server()








