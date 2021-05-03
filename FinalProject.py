# -*- coding: utf-8 -*-
"""
Created on Mon May  3 10:16:40 2021

@author: adaxm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore")
df = pd.read_csv(r'C:\Users\adaxm\Downloads\country_vaccinations_by_manufacturer.csv')
print(df)
df["date"]= pd.to_datetime(df.date)

df["total_vaccinations(count)"]= df.groupby("location").total_vaccinations.tail(1)

df.groupby("location")["total_vaccinations(count)"].mean().sort_values(ascending= False).head(20)

#barplot visualization of top countries with most vaccinations
x= df.groupby("location")["total_vaccinations(count)"].mean().sort_values(ascending= False).head(20)
sns.set_style("whitegrid")
plt.figure(figsize= (8,8))
ax= sns.barplot(x.values,x.index)
ax.set_xlabel("total_vaccinations(count)")
plt.title('Top countries with most vaccinations')
plt.xlabel('Total vaccinations')
plt.ylabel('Countries')
plt.show()


#Total vaccinations in United States
plt.figure(figsize= (15,5))
sns.lineplot(x= "date",y= "total_vaccinations",data= df[df["location"]=="United States"])
plt.title('Total vaccinations in United States')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.show()


#daily vaccination comparison between countries
plt.figure(figsize= (15,5))
sns.lineplot(x= "location",y= "date" ,data= df,hue= "vaccine")
plt.title('Vaccines by Location')
plt.show()

#Manufacturer
x= df.groupby("vaccine")["total_vaccinations(count)"].mean().sort_values(ascending= False).head(20)
sns.set_style("whitegrid")
plt.figure(figsize= (6,6))
ax= sns.barplot(x.values,x.index)
ax.set_xlabel("total_vaccinations(count)")
plt.title('The most used vaccines')
plt.xlabel('Total vaccinations')
plt.ylabel('Countries')
plt.show()

#Top 5
x= df.loc[(df.location== "United States") | (df.location== "Germany")| (df.location== "France")| (df.location== "Italy")|(df.location== "China")]
plt.figure(figsize= (15,5))
sns.lineplot(x= "date",y= "total_vaccinations" ,data= df,hue= "location")
plt.title('Top 5 vaccinated countries')
plt.show()


import dash
import dash_bootstrap_components as dbc

#Instantiates the Dash app and identify the server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#INDEX

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server 
#import your navigation, styles and layouts from layouts.py here
from layouts import nav_bar, layout1, CONTENT_STYLE 
import callbacks

# Define basic structure of app:
# A horizontal navigation bar on the left side with page content on the right.
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), #this locates this structure to the url
    nav_bar(),
    html.Div(id='page-content',style=CONTENT_STYLE) #we'll use a callback to change the layout of this section 
])

# This callback changes the layout of the page based on the URL
# For each layout read the current URL page "http://127.0.0.1:5000/pagename" and return the layout
@app.callback(Output('page-content', 'children'), #this changes the content
              [Input('url', 'pathname')]) #this listens for the url in use
def display_page(pathname): #ADD PAGES#
    if pathname == '/':
        return layout1
    elif pathname == 'Data and Graphs':
        return layout1
    else:
        return '404' #If page not found return 404

#Runs the server

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    #LAYOUTS
    
    import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import plotly.express as px


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#####################################
# Add your data
#####################################

#example iris dataset
dff = px.data.iris()

df = pd.read_csv(r'C:\Users\adaxm\Downloads\country_vaccinations_by_manufacturer.csv')

#####################################
# Styles & Colors
#####################################

NAVBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "top":0,
    "margin-top":'2rem',
    "margin-left": "18rem",
    "margin-right": "2rem",
}

#####################################
# Create Auxiliary Components Here
#####################################

def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = html.Div(
    [
        html.H4("Covid-19 vaccination by manufacturer 2021", className="display-10",style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Page 1", href="/page1",active="exact", external_link=True), #CORRESPONDING TO INDEX#
            ],
            pills=True,
            vertical=True
        ),
    ],
    style=NAVBAR_STYLE,
    )  
    return navbar

#graph 1
df["date"]= pd.to_datetime(df.date)

df["total_vaccinations(count)"] = df.groupby("location").total_vaccinations.tail(1)
x= df.groupby("location")["total_vaccinations(count)"].mean().sort_values(ascending= False).head(20)
example_graph1 = px.bar(df, x="total_vaccinations(count)", y="location", title="Total vaccination by Country")

#graph 2

plt.figure(figsize= (15,5))
sns.lineplot(x= "date",y= "total_vaccinations",data= df[df["location"]=="United States"])
example_graph2 = sns.lineplot(x= "date",y= "total_vaccinations",data= df[df["location"]=="United States"])



#example_graph2 = px.histogram(dff, x="sepal_length", color = "species",nbins=20)
#example_graph2.update_layout(barmode='overlay')
#example_graph2.update_traces(opacity=0.55)

#graph 3. Daily vaccination comparison between countries
plt.figure(figsize= (15,5))
sns.lineplot(x= "location",y= "date" ,data= df,hue= "vaccine")
plt.title('Vaccines by Location')
plt.show()
example_graph3 = sns.lineplot(x= "location",y= "date" ,data= df)

#Graph 4. Manufacturer
x= df.groupby("vaccine")["total_vaccinations(count)"].mean().sort_values(ascending= False).head(20)
sns.set_style("whitegrid")
plt.figure(figsize= (6,6))
ax= sns.barplot(x.values,x.index)
ax.set_xlabel("total_vaccinations(count)")
plt.title('The most used vaccines')
plt.xlabel('Total vaccinations')
plt.ylabel('Countries')
plt.show()
example_graph4 = px.bar(df, x="total_vaccinations(count)", y="vaccine", title="The most used vaccines")

#Graph 5. Top 5
x= df.loc[(df.location== "United States") | (df.location== "Germany")| (df.location== "France")| (df.location== "Italy")|(df.location== "China")]
plt.figure(figsize= (15,5))
sns.lineplot(x= "date",y= "total_vaccinations" ,data= df, hue= "location")
plt.title('Top 5 vaccinated countries')
example_graph5 = px.bar(df, x="date", y="total_vaccinations", title="Top vaccinated countries")

#####################################
# Create Page Layouts Here
#####################################

### Layout 1
layout1 = html.Div([
    html.H2("Data and Graphs"),
    html.Hr(),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                            html.H4('Example Graph Page'),
                            #create tabs
                            dbc.Tabs(
                                [
                               #graphs will go here eventually using callbacks
                                    dbc.Tab(label='Most Vaccinated Countries',tab_id='Most Vaccinated Countries'),
                                    dbc.Tab(label='USA',tab_id='USA'),
                                    dbc.Tab(label='Daily vaccinations',tab_id='Daily vaccinations'),
                                    dbc.Tab(label='Manufacturer',tab_id='Manufacturer'),
                                    dbc.Tab(label='Top 5',tab_id='Top 5'),
                                    
                                    #dbc.Tab(label='graph5',tab_id='graph5'),
                                    #dbc.Tab(label='graph6',tab_id='graph6'),
                                    #dbc.Tab(label='graph7',tab_id='graph7')
                                    
                                ],
                                id="tabs",
                                active_tab='graph1',
                                ),
                            html.Div(id="tab-content",className="p-4")
                            ]
                        ),
                    ],
                    width=6 #half page
                ),
                
                dbc.Col(
                    [
                        html.H4('Additional Components here'),
                        html.P('Click on graph to display text', id='graph-text')
                    ],
                    width=6 #half page
                )
                
            ],
        ), 
    ]),
])

#CALLBACKS

# @app.callback(
#     Output("component-id-to-output-to", "children"),
#     Input("component-id-to-listen-to", "valuesIn")
# )
# def callback_name(valuesIn):
#     #code for callback to execute
#     return output_to_children


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from layouts import example_graph1, example_graph2, example_graph3, example_graph4, example_graph5
from app import app

#import graphs that you need to show
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, and 
    renders the associated graph with the tab name on page 1.
    """
    if active_tab is not None:
        if active_tab == "Info":
            return html.Div([html.P('We will remember coronavirus for a long time as our society got affected worldwide adapting to a new normal. It was a global pandemic causing transformations to the daily life. The World Health Organization declared a Public Health Emergency of International Concern regarding COVID-19 on 30 January 2020, and later declared a pandemic on March 2020. We have been in lockdown for more than a year and as off now, May 2021 most of the countries are offering doses of vaccines to their citizens. For the final project of MA705 class I wanted to show a dashboard with visualizations using python concepts to represent a summary of data and graphs for Covid-19 vaccination by manufacturer.'),dcc.Graph(figure=example_graph1, id='graph')])
        elif active_tab == "USA":
            return dcc.Graph(figure=example_graph2, id='graph')        
        elif active_tab == "Daily vaccinations":
            return dcc.Graph(figure=example_graph3, id='graph')
        elif active_tab == "Manufacturer":
            return dcc.Graph(figure=example_graph4, id='graph')
        elif active_tab == "Top 5":
            return dcc.Graph(figure=example_graph5, id='graph')       
    return "No tab selected"

@app.callback(
    Output("graph-text","children"),
    Input("graph","clickData"),
)
def graph_click(clickData):
    """
    This callback identifies if the clicked upon graph is a scatter plot 
    or a historgram and displays data clicked on
    """
    if 'pointIndex' in clickData['points'][0]:
        return html.P(f"Sepal Length: {clickData['points'][0]['x']}\nSepal Width: {clickData['points'][0]['y']}")
    elif 'binNumber' in clickData['points'][0]:
        return html.P(f"Sepal Length: {clickData['points'][0]['x']}\nCount: {clickData['points'][0]['y']}")

@app.callback(
    Output("selected-button","children"),
    Input("page2-buttons","value")
)
def button_choice(value):
    """
    This callback takes in page2-buttons selected value and returns content to display
    in selected-button
    """
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output("selected-dropdown","children"),
    Input("page2-dropdown","value")
)
def dropdown_choice(value):
    """
    This callback takes in page2-dropdown's selected value and returns content to display
    in selected-button
    """
    return 'You have selected "{}"'.format(value)