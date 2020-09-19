import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import altair as alt

st.title("  📍 Homework Streamlit  👩🏼‍💻 🌎")
st.markdown(
"""
นางสาว  รวิสรา  ไกรลาศรัตนศิริ  รหัสนิสิต 6030492721 
""")
DATA_URL = ("data_5_months.xlsx")
@st.cache(persist=True)
def load_data():
    data = pd.read_excel(DATA_URL,parse_dates=['time'])
    data.dropna(subset=['latitude', 'longitude'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data

data=load_data()
data=data.drop(columns = ['unnamed: 0'])
DATE_TIME = "time"


st.header("Select Month")
select = st.selectbox('Month', ['All','Jan', 'Feb', 'Mar', 'Apr','May'])


if select == 'Jan':
    data = data[data[DATE_TIME].dt.month == 1]

elif select == 'Feb':
    data = data[data[DATE_TIME].dt.month == 2]
    

elif select == 'Mar':
    data = data[data[DATE_TIME].dt.month == 3]
    
elif select == 'Apr':
    data = data[data[DATE_TIME].dt.month == 4]
    
elif select == 'May':
    data = data[data[DATE_TIME].dt.month == 5]
    
else:
    data = data
    
hour = st.slider("Hour to look at", 0, 23)
data_show = data[data[DATE_TIME].dt.hour == hour]

options = st.radio('Select Start-Stop', ('Start','Stop',"All"))

if options == 'Start' :
    data_1 = data_show[data_show["flag"]== 'Start']
elif options=="Stop" :
    data_1 = data_show[data_show["flag"]=="Stop"]
else :
    data_1 = data_show

st.write(data_1)

st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data_1["latitude"]), np.average(data_1["longitude"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data_1,
            get_position=["longitude", "latitude"],
            auto_highlight = True,
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data_1[
    (data_1[DATE_TIME].dt.hour >= hour) & (data_1[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)


