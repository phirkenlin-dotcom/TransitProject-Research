import streamlit as st
import pandas as pd

distance = pd.read_csv("Distance.csv")


import streamlit as st

st.title("Congressional District 35: Public Transit & Schools Analysis")
st.write("This analysis explores public transit accessibility for local schools in our district.")
st.header("1. Overview: Distance of Transit Stations by School")
col1, col2 = st.columns(2)

with col1:
    df = pd.read_csv("Distance.csv")
    st.dataframe(df, use_container_width=True)

with col2:
       st.image("Distance of Transit Station by School Name.jpg", caption="Distance of Transit Station by School Name")

st.header("2. Geographic Map View")
st.image("School with Bus Stop Map.jpg", caption="Map of Schools (Blue) and Transit Stops (Orange)")

st.header("3. Focus Area: Schools More Than 0.5 Miles Away")
st.write("These schools face the greatest distance from public transit options.")
st.image("Schools With Bus Stops More Than 0.5 Miles away by School Name.jpg", caption="Schools with Bus Stops > 0.5 Miles Away")
