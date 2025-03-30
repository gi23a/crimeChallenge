import pandas as pd
import plotly.express as express
import plotly.io as io





def map_build(data , mapType):

    #only use sample from the data :
    if mapType == "category":
        data = data[["Latitude real (Y)", "Longitude real (X)", "Address" , "Category"]].dropna().sample(3000, random_state=42)

        fig = express.scatter_mapbox(
        data,
        lat="Latitude real (Y)",
        lon="Longitude real (X)",
        color="Category",
        zoom=10,
        hover_name="Category", 
        hover_data=["Address"],
        mapbox_style="open-street-map", 
        #fig.write_html("crime_map_final.html")
        )
    elif mapType == "heatmap":
        data = data[["Latitude real (Y)", "Longitude real (X)", "Address" ]].dropna().sample(3000, random_state=42)

        fig = express.density_mapbox(
            data,
            lat="Latitude real (Y)",
            lon="Longitude real (X)",
            radius=8,
            center=dict(
                lat=data["Latitude real (Y)"].mean(),
                lon=data["Longitude real (X)"].mean()
            ),
            zoom=11,
            mapbox_style="open-street-map",
            color_continuous_scale="RdYlGn_r",
            title="Crime Hotspot Heatmap",
            hover_data=["Address"]
        )

    elif mapType == "single":
        fig = express.scatter_mapbox(
            data,
            lat="Latitude real (Y)",
            lon="Longitude real (X)",
            zoom=10,
            hover_name="Address",  
            hover_data=["Address"], 
            mapbox_style="open-street-map", 
            
        )
        fig.update_traces(marker=dict(size=12))
    else:
        raise ValueError("error when building the map ")
    fig.update_layout(height=700, width=1000)
    return fig

