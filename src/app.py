#importing the libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, dash_table


# importing the excel file
excel_file = pd.ExcelFile(r"Monthly order report vaayu to production.xlsx")

#print(excel_file.sheet_names)

# initializing an empty list to store the dataframes created from sheets of the excel file
df_list = []

for i in range(len(excel_file.sheet_names)):
    data = pd.read_excel(excel_file,excel_file.sheet_names[i])
    df_list.append(data)
    
# creating the date, month and week of month columns
vaayu_production_data = pd.concat([i for i in df_list],axis=0)
vaayu_production_data["DATE"]=pd.to_datetime(vaayu_production_data["DATE"])
vaayu_production_data["Month Name"]=vaayu_production_data["DATE"].dt.month_name()
vaayu_production_data["Week Number"]=vaayu_production_data["DATE"].dt.day.apply(lambda x: (x-1)//7 +1)
vaayu_production_data["Week Number"]=vaayu_production_data["Week Number"].apply(lambda x: "Week "+str(x))

#print(vaayu_production_data)
#print("\n _____ \n", vaayu_production_data.dtypes)


## building the dash application

app = Dash(__name__)
server=app.server


app.layout=html.Div([
    html.H1("Vaayu Production Data"),
    html.H3("Please select parameters"),
    dcc.Dropdown(options=vaayu_production_data.columns,value=["Month Name","Week Number"],id="dropdown-1",multi=True),
    dcc.Graph(id="graph-1")
    
])

@callback(
    Output("graph-1","figure"),
    Input("dropdown-1","value")
)

def update_graph(value1):
    columns=value1
    fig=px.sunburst(vaayu_production_data,path=columns,values="QUANTITY",height=700,width=1000)
    fig.update_traces(textinfo="label+value")
    
    return fig

if __name__=="__main__":
    app.run(debug=True)