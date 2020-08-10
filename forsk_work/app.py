# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:16:13 2020

@author: user
"""
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, State, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_table as dt
import dash_table
import webbrowser
from threading import Timer
import dash_bootstrap_components as dbc
import os
import math
import sys
pd.options.mode.chained_assignment = None
meeting_id = 89261554713

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')
      
      

      
      
external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


if os.path.exists("{}.txt".format(meeting_id)):
    markdown_list = []
    
    try:
        f= open("{}.txt".format(meeting_id), 'r')
        while True:
            # read line
            line = f.readline()
            markdown_list.append(line)
            # check if line is not empty
            if not line:
                break
    except (IOError, ValueError, EOFError) as e:
      print(e)
    f.close()
    
    
    all_lines = "\n".join(markdown_list)[:-1]
    
    
    markdown_text = '''
    {}
    '''.format(all_lines)
else:
    markdown_text = '''
    
    '''


list1 = ["Day0","Day1","Day2","Day3","Day4","Day5"]

df1 = pd.read_csv("Full_data_present_everyday.csv")
df2 = pd.read_csv("Not_present_any_day.csv")

list2 = ['Registered Name','Email','Gender','College Name','WhatsApp No.']



colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'color1': 'white',
    'color2': 'blue'
}

fig1=px.bar(df1, y ='Total',x = 'Zoom Name',
                text='Total',
                color='Total',
                hover_data=['Name','Gender','College Name','Email','WhatsApp No.','Day0','Day1','Day2','Day3','Day4','Day5'],
                height=450,
            )


list3 = ['Name_Reg','Email','Gender_Reg','College Name_Reg','WhatsApp No._Reg']

list4 = ['Name','Gender','College Name','Email','WhatsApp No.','Day0','Day1','Day2','Day3','Day4','Day5']
app.title = str(meeting_id)

#app.head = [
#    html.Link(
#        href='https://www.google.com/favicon.ico',
#        rel='icon'
#    ),
#]



PAGE_SIZE = 5


app.layout = html.Div(
        html.Div([
                dbc.Container(
                html.Div(
                [
                html.Img(
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSriyJq1c35TlZ9DIJQrV4ELxG914tFyXLVKQ&usqp=CAU",
                    className='three columns',
                    style={
                        'height': '15%',
                        'width': '26%',
                        'float': 'center',
                        'position': 'relative',
                        'padding-top': 0,
                        'margin-left': 360,
                        'textAlign': 'center'
                    },
                ),
            ], className="row"
        ),
    ),



   html.Div(children=[
        
    
    
    html.H1(
        children='Forsk Coding School',
        style={
            'textAlign': 'center',
            'color': colors['color1'],
            'backgroundColor': colors['color2'],
            'borderRadius': '5px',
            'margin': '20px',
            'padding': '10px',
            'margin-bottom':'-6px',
            'font-size': '40px',
            'margin-top':'10px'
            
        }
    ),
    html.H3(
        children=' Student Attendence Analysis ',
        style={
            'textAlign': 'center',
            'color': colors['color1'],
            'backgroundColor': colors['color2'],
            'borderRadius': '5px',
            'margin': 'auto',
            'margin-right':'20px',
            'margin-left':'20px',
            'font-size': '18px',
            'padding': '10px',
        }
    ),
    
    
    #Markdown (details of Prime)
    html.Div([dcc.Markdown(children=markdown_text)],
              style={
            'textAlign': 'center',
            'font-size': '23px',
            'font-family': "Comic Sans MS",
            
        }
        
    ),
    
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





    #Present Registered student
    html.Div([
            html.Div(
                        [
                            html.H3(
                                children='Registered & Participants',
                                style={
                                    'textAlign': 'Right',
                                    'color': colors['color2'],
                                    'margin': 'auto',
                                    'font-size': '25px',
                                    'margin-bottom':'0px',
                                    'font': '20px Arial, sans-serif',
                                    
                                }
                            ),
                            ],className='seven columns',
                        style={'padding-top': '30px'}
            ),
           html.Div(
                        [
                            html.H3(
                                children='Count: ',
                                style={
                                    'textAlign': 'Right',
                                    'color': colors['color2'],
                                    'margin': 'auto',
                                    'font-size': '25px',
                                    'margin-bottom':'0px',
                                    'font': '20px Arial, sans-serif',
                                    
                                }
                            ),
                        ],
                        className='three columns',
                        style={'padding-top': '30px'}
                    ),
            html.Div(
                        [
                            html.H3(
                                id = 'check_count_present',
                                style={
                                    'textAlign': 'Left',
                                    'color': colors['color2'],
                                    'margin': 'auto',
                                    'font-size': '25px',
                                    'margin-bottom':'0px',
                                    'font': '20px Arial, sans-serif',
                                    
                                }
                            ),
                        ],
                        className='two columns',
                        style={'padding-top': '30px'}
                    )
        ],className = 'row'
    ),
    
    
    
    html.H3(
            id = 'reg',
        style={
            'textAlign': 'center',
            'color': 'black',
            'margin': 'auto',
            'font-size': '25px',
            'margin-bottom':'0px',
            'font': '20px Arial, sans-serif',
            
        }
    ),
    #graph1
    dcc.Graph(id = 'graph'),
    
    
    
    
    
    
    
    #Absent Students
    html.H3(
        children='Absent Students Table',
        style={
            'textAlign': 'center',
            'color': colors['color2'],
            'margin': 'auto',
            'font-size': '25px',
            'margin-bottom':'0px',
            'margin-top':'70px',
            'font': '20px Arial, sans-serif',
        }
    ),
    
    
    
    #Table
    html.Div(
            [
                    
                dash_table.DataTable(
                id='datatable-paging',
                columns=[
                    {"name": i, "id": i} for i in list2],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action='custom',
                style_table={
                        'overflowX': 'auto'},
               style_cell={'textAlign': 'left',
                           'height': 'auto',
                           'minWidth': '500px', 'width': '500px', 'maxWidth': '500px',
                           'whiteSpace': 'normal'}, 
               style_data={ 'border': '1px solid blue' ,
                           'margin-left':'20px',
                           'margin-right':'20px'},
                style_header={
                  'backgroundColor': 'rgb(230, 230, 230)',
                  'fontWeight': 'bold'
            },
              
#                        style={
#            'textAlign': 'center',
#            'color': colors['color2'],
#            'margin': 'auto',
#             }
                ),
                
                
            ], className = 'row'
        ),
    
    
    
    
    
    #Not Registered student
    html.H3(
        children='UnRegistered But Present',
        style={
            'textAlign': 'center',
            'color': colors['color2'],
            'margin': 'auto',
            'font-size': '25px',
            'margin-bottom':'0px',
            'margin-top':'70px',
            'font': '20px Arial, sans-serif',
        }
    ),
    
    #graph3
    dcc.Graph(id = 'graph3'),
    
    
    
    #Not present any day student
    html.H3(
        children='Full present students',
        style={
            'textAlign': 'center',
            'color': colors['color2'],
            'margin': 'auto',
            'font-size': '25px',
            'margin-bottom':'0px',
            'margin-top':'70px',
            'font': '20px Arial, sans-serif',
        }
    ),
    
   #=========================================================================================
   
   
   
   
   
     #graph4           
    dcc.Graph(figure=fig1),
        
        
        #Full data present
        html.H3(
            children='Not present any day student',
            style={
                'textAlign': 'center',
                'color': colors['color2'],
                'margin': 'auto',
                'font-size': '25px',
                'margin-bottom':'0px',
                'margin-top':'70px',
                'font': '20px Arial, sans-serif',
            }
        ),
        
         html.Div(
            [
                    
                dash_table.DataTable(
                id='not_present_table',
                columns=[
                    {"name": i, "id": i} for i in list3],
               page_current=0,
               page_size=PAGE_SIZE,
               page_action='custom',
               style_cell={'textAlign': 'left'}, 
               style_data={ 'border': '1px solid blue' ,
                           'margin-left':'20px',
                           'margin-right':'20px'},
                style_header={
                  'backgroundColor': 'rgb(230, 230, 230)',
                  'fontWeight': 'bold'
            },
              
#                        style={
#            'textAlign': 'center',
#            'color': colors['color2'],
#            'margin': 'auto',
#             }
                ),
                
                
            ], className = 'row'
        ),
           

        #search data             
        html.Div([
            dcc.Store(id = 'memory'),
            html.H3('Details of Particular Student:'),
            html.Div(
                [
                    html.Div(
                        [
                            html.P('Search by:'),
                            dcc.Dropdown(
                                    id = 'filter_x',
                                    options=[
                                        {'label': 'No filter', 'value': 0},
                                        {'label': 'Name', 'value': 1},
                                        {'label': 'Email id', 'value': 2},
                                        {'label': 'Mobile No.', 'value': 3},
                                        {'label': 'College Name', 'value': 4}
                                    ],
                                    value='0'
                                 ),
                        ],
                        className='three columns',
                        style={'margin-top': '10'}
                    ),
                    html.Div(
                        [
                            html.P('Select one:'),
                            dcc.Dropdown(
                                    id = 'filter_z',
                                    options=[
                                        {'label': 'No filter', 'value': 0},
                                        {'label': 'Start With', 'value': 1},
                                        {'label': 'Ends With', 'value': 2}
                                    ],
                                    value='0'
                                 ),
                        ],
                        className='three columns',
                        style={'margin-top': '10'}
                    ),
                    html.Div(
                        [
                            html.P('Search From Here: '),
                            dcc.Input(
                                      id = 'filter_y',
                                      placeholder='Enter a value...',
                                      value=''
                                  )  ,
                        ],
                        className='four columns',
                        style={'margin-top': '10','padding-left': '70px'}
                    ),
                    html.Div(
                        [
                            html.Button(children='Search Data', id='button_chart',n_clicks=0)
                        ],
                        className='two columns',
                        style={'padding-top': '30px'}
                    )             
                ],
                className='row'
            ),
             html.Div(
                [
                      
                        
                    dash_table.DataTable(
                    id='table',
                    columns=[
                        {"name": i, "id": i} for i in list4],
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='custom',
                    style_table={
                        'overflowX': 'auto'},
                    style_cell={'height': 'auto',
                                   'textAlign': 'left',
                                   'minWidth': '200px', 'width': '200px', 'maxWidth': '180px',
                                   'whiteSpace': 'normal'},  
                    
                    style_data={ 'border': '1px solid blue' ,
                               'margin-left':'20px',
                               'margin-right':'20px'},
                    style_header={
                      'backgroundColor': 'rgb(230, 230, 230)',
                      'fontWeight': 'bold'},
                    ),
                    
                    
                            
                            
                 ], className = 'row',style = {'margin-top': 40,}
              ),

           ], className = 'row',  style = {'margin-top': 50, 'border':
                                    '1px solid #C6CCD5', 'padding': 15,
                                    'border-radius': '5px'}
        ),
                    
       

      #footer part
      html.H3(
        children='Footer Section',
        style={
            'textAlign': 'center',
            'color': colors['color1'],
            'backgroundColor': colors['color2'],
            'borderRadius': '2px',
            'padding': '70px',
            'margin-bottom':'0',
            'font-size': '20px',
            'margin-top':'20px'
            
        }
    ),             
                    
     
]),
    
])
)



@app.callback(dash.dependencies.Output('reg','children'),[dash.dependencies.Input('dd','value')])
def update_fig(value):  
    return value


@app.callback([dash.dependencies.Output('graph','figure'),
              dash.dependencies.Output('check_count_present','children')],
              [dash.dependencies.Input('dd','value')])

def update_fig(value):
    try:
    
        dff = pd.read_csv("{}.csv".format(value))
        a = dff[(dff["Email"].isnull())].index[0]
        dff = dff.iloc[:a,]
        count = len(dff)
        dff.rename(columns={'Time':'Time(Minutes)'}, inplace = True )
        figure = px.bar(dff, y ='Time(Minutes)',x = 'Registered Name',
                        text='Time(Minutes)',
                        hover_data=['Registered Name','Gender','College Name','Email'],
                        height=650,
                        )
        figure.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        figure.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        
#        figure = {
#            'data':[
#            {'x': dff['Zoom Name'], 'y': dff['Time'], 'type': 'bar', 'name': 'SF'}
#            ],
#        'layout':{
#                'title' : 'Every student spend Time on Zoom',
#                'margin':{'t':0,'b':180},
#                'plot_bgcolor': colors['background'],
#                'paper_bgcolor': colors['background'],
#                'font': {
#                        'color': colors['text']
#                    }
#                
#            }
#        }
    except:
        return html.Div(['There was an error processing this file.'])
        
    return figure,count






@app.callback([dash.dependencies.Output('datatable-paging','data'),
               dash.dependencies.Output('datatable-paging','page_count')],
              [dash.dependencies.Input('dd','value'),
               dash.dependencies.Input('datatable-paging', "page_current"),
               dash.dependencies.Input('datatable-paging', "page_size")])

def update_fig(value,page_current,page_size):
    try:
        dff = pd.read_csv("{}.csv".format(value))
        a = dff[(dff["Email"].isnull())].index[0]
        b = dff[(dff["Email"].isnull())].index[1]
        dff = dff.iloc[a+2:b,]
        page_count_value = math.ceil(len(dff)/5)
        data=dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
        return data,page_count_value
              

    except:
        return html.Div(['There was an error processing this file.'])
        
   


@app.callback([dash.dependencies.Output('not_present_table','data'),
               dash.dependencies.Output('not_present_table','page_count')],
              [dash.dependencies.Input('not_present_table', "page_current"),
               dash.dependencies.Input('not_present_table', "page_size")])

def update_fig(page_current,page_size):
    try:
        df3 = pd.read_csv("Not_present_any_day.csv")
        page_count_value = math.ceil(len(df3)/5),
        data=df3.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
        return data,page_count_value
              

    except:
        return html.Div(['There was an error processing this file.'])





@app.callback(dash.dependencies.Output('graph3','figure'),[dash.dependencies.Input('dd','value')])

def update_fig(value):
    try:
        dff = pd.read_csv("{}.csv".format(value))
        b = dff[(dff["Email"].isnull())].index[1]
        dff = dff.iloc[b+2:,]
        figure = px.bar(dff, y ='Time',x = 'Zoom Name',
                        text='Time',
                        color='Time',
                        hover_data=['Email'],
                        height=500)
        figure.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        figure.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
              

    except:
        return html.Div(['There was an error processing this file.'])
        
    return figure
    
#import plotly.express as px
#
#df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
#fig = px.bar(df, y='pop', x='country', text='pop')
#fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
#fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
#fig.show()
#             
    

@app.callback(dash.dependencies.Output('filter_y','type'),[dash.dependencies.Input('filter_x','value')])

def drop_value(value):
    if value == 1:
        type = "text"
        return type
    elif value == 2:
        type = "email"
        return type
    elif value == 3:
        type = "number"
        return type
    elif value == 4:
        type = "text"
        return type
    elif value == 0:
        type = "text"
        return type


@app.callback(dash.dependencies.Output('table', 'data'),
                [dash.dependencies.Input('filter_x','value'),
                 dash.dependencies.Input('filter_z','value'),
                 dash.dependencies.Input('table', "page_current"),
                 dash.dependencies.Input('table', "page_size"),
                 dash.dependencies.Input('button_chart', 'n_clicks')],
                [dash.dependencies.State('filter_y', 'value')])


def update_figure(value1,value2,page_current,page_size,n_clicks, filename):
    df5 = pd.read_csv("Full_data_present_everyday.csv")
    if value2 == 1:
        if value1 == 3:
#            if type(filename) == int:
                filename = str(filename)
                filename_list = []
                for index,number in enumerate(df5["WhatsApp No."].tolist()):
                    if filename in str(number):
                        if str(number).startswith(filename):
                                filename_list.append(index)
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
        elif value1 == 1:
#            if filename.isalpha():
                filename = filename.upper()
                filename_list = []
                for index,name in enumerate(df5["Name"].tolist()):
                    if filename in name:
                        name1 = name.split()
                        for name1_part in name1:
                            if name1_part.startswith(filename):
                                filename_list.append(index)
                                break
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
    
        elif value1 == 2:
#            if filename.isalnum() or filename.isalpha() or filename.isdigit() or "@" in filename or "." in filename:
                filename = filename.upper()
                filename_list = []
                for index,email in enumerate(df5["Email"].tolist()):
                        if email.upper().startswith(filename):
                            filename_list.append(index)
                            
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data=df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
        
        
        elif value1 == 4:
#            if filename.isalnum() or filename.isalpha() or filename.isdigit():
                filename = filename.upper()
                filename_list = []
                for index,name in enumerate(df5["College Name"].tolist()):
                    if filename in name.upper():
                        name1 = name.upper().split()
                        for name1_part in name1:
                            if name1_part.startswith(filename):
                                filename_list.append(index)
                                break
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
    elif value2 == 2:
        if value1 == 3:
#            if type(filename) == int:
                filename = str(filename)
                filename_list = []
                for index,number in enumerate(df5["WhatsApp No."].tolist()):
                    if filename in str(int(number)):
                        if str(int(number)).endswith(filename):
                                filename_list.append(index)
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
        elif value1 == 1:
#            if filename.isalpha():
                filename = filename.upper()
                filename_list = []
                for index,name in enumerate(df5["Name"].tolist()):
                    if filename in name:
                        name1 = name.split()
                        for name1_part in name1:
                            if name1_part.endswith(filename):
                                filename_list.append(index)
                                break
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
    
        elif value1 == 2:
#            if filename.isalnum() or filename.isalpha() or filename.isdigit() or "@" in filename or "." in filename:
                filename = filename.upper()
                filename_list = []
                for index,email in enumerate(df5["Email"].tolist()):
                        if email.upper().endswith(filename):
                            filename_list.append(index)
                            
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data=df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data
        
        
        elif value1 == 4:
#            if filename.isalnum() or filename.isalpha() or filename.isdigit():
                filename = filename.upper()
                filename_list = []
                for index,name in enumerate(df5["College Name"].tolist()):
                    if filename in name.upper():
                        name1 = name.upper().split()
                        for name1_part in name1:
                            if name1_part.endswith(filename):
                                filename_list.append(index)
                                break
                df6 = []
                for i in filename_list:
                    df6.append(df5.iloc[i])
                df7 = pd.DataFrame(df6)
                data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                return data   
    else:
        if n_clicks:
            data = df5.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
            return data
    


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    