### YOUR IMPORTS HERE ###
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def query_climate(df, country: str, year_begin: int, year_end: int, month: int) -> pd.DataFrame:
    sample = df.loc[(df["Country"]==country) & (df["Year"]>=year_begin) & (df["Year"]<=year_end)]
    output = sample[["NAME", "LATITUDE", "LONGITUDE", "Country", "Year"]].copy()
    output.loc[:, "Month"] = month
    output.loc[:, "Temp"] = sample.iloc[:, month+1]
    return output

def get_mean_temp(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> pd.DataFrame:
    sample = query_climate(df, country, year_begin, year_end, month)
    temp_mean = sample.groupby(["NAME", "LATITUDE", "LONGITUDE"])[["Temp"]].mean().round(2)
    output = pd.merge(sample, temp_mean, on = ["NAME", "LATITUDE", "LONGITUDE"], how = "left")
    output = output.rename(columns = {"Temp_x":"Temp", "Temp_y":"Mean_Temp"})
    return output

def temperature_plot(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> go.Figure:
    sample = get_mean_temp(df, country, year_begin, year_end, month)
    fig = px.scatter_map(sample, 
                         lat = "LATITUDE",
                         lon = "LONGITUDE",
                         hover_name = "NAME",
                         zoom = 4,
                         height = 300,
                         color = "Mean_Temp",
                         color_continuous_scale = "Inferno",
                         map_style="open-street-map", 
                         title = "Average Temperature at Each Station in " + country + " from " + str(year_begin) + " to " + str(year_end) + " during Month " + str(month)) 
    fig.update_layout(margin={"r":50, "t":40, "l":20, "b":25})
    fig.update_layout(title={'font': {'size': 12}})
    return fig