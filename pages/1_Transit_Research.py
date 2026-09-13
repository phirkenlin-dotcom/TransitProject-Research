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
    st.dataframe(df, use_container_width=True, height=400)

with col2:
       st.image("Distance of Transit Station by School Name.jpg", caption="Distance of Transit Station by School Name",
              use_container_width=True)

st.header("2. Geographic Map View")
st.image("School with Bus Stop Map.jpg", caption="Map of Schools (Blue) and Transit Stops (Orange)")

# st.header("3. Focus Area: Schools More Than 0.5 Miles Away")
st.write("These schools face the greatest distance from public transit options.")
st.image("Schools With Bus Stops More Than 0.5 Miles away by School Name.jpg", caption="Schools with Bus Stops > 0.5 Miles Away")

st.header("Data Sources")
st.write("For this analysis I used various data which is publically available. Below are the key sources that I used for my analysis.")
st.markdown("""
- [OmniRide Developer Tools](https://www.omniride.com/contact/developer-tools/)
- [Foothill Transit Developer Resources](https://www.foothilltransit.org/developer-resources)
- [Rep. Torres — GovTrack Profile (CA District 35)](https://www.govtrack.us/congress/members/CA/35)
- [California Senate District Mapping — District 35](https://sdmg.senate.ca.gov/committeehome/2025-congressional-districts/congressional-district-35-2025)
""")
