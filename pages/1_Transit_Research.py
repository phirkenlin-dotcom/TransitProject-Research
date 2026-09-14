import streamlit as st
import pandas as pd

distance = pd.read_csv("Distance.csv")


import streamlit as st

st.title("Congressional District 35: Public Transit & Schools Analysis")
st.write("This analysis explores public transit accessibility for local schools in our district.")

st.subheader("Background & Motivation :")
st.write("""
While serving on Congresswoman Norma Torres' Advisory Committee, I became interested in how transportation affects California's 35th Congressional District. I noticed many students used public transit and I wanted to investigate if the schools in the district had access to buses. Additionally, as someone who used to live in the Netherlands until I was 8, public transit had always been a big part of my life there, and I wished to bring that to my community.

This naturally led me to the overarching research question:
Do students in California's 35th Congressional District have equitable access to public transportation, and where should new bus stops be placed to improve access to middle and high schools?
""")


st.subheader("1. Overview: Distance of Transit Stations by School")
st.write("""
To evaluate transit equity across the district, I conducted a walking-distance analysis for 36 middle and high schools in the district. Using coordinates for each school and bus stop and the Haversine formula, I calculated the distance from each school to its nearest active bus stop to determine which campuses have strong transit connections and which face access gaps.
""")

col1, col2 = st.columns(2)

with col1:
    df = pd.read_csv("Distance.csv")
    st.dataframe(df, use_container_width=True, height=400)

with col2:
       st.image("Distance of Transit Station by School Name.jpg", caption="Distance of Transit Station by School Name")

st.header("2. Geographic Map View")
st.image("School with Bus Stop Map.jpg", caption="Map of Schools (Blue) and Transit Stops (Orange)")

# st.header("3. Focus Area: Schools More Than 0.5 Miles Away")
st.write("I analyzed about 36 High Schools and Middle Schools in Congressional District 35.I observed that nearly 86% i.e.31 schools are within 0.5 miles of walking distrance.Whereas 5 schools has distance greater than 0.5 miles to or from public transit options")
st.write("Whereas 5 schools face the greatest distance from public transit options.")
col1, col2 = st.columns(2)

with col1:
       st.image("Schools By Walking Distances.jpg", caption="Overview of Schools by Distance of Transit Station")
with col2:
       st.image("Schools With Bus Stops More Than 0.5 Miles away by School Name.jpg", caption="Schools with Bus Stops > 0.5 Miles Away")



st.header("Data Sources")
st.write("For this analysis I used various data which is publically available. Below are the key sources that I used for my analysis.")
st.markdown("""
- [OmniRide Developer Tools](https://www.omniride.com/contact/developer-tools/)
- [Foothill Transit Developer Resources](https://www.foothilltransit.org/developer-resources)
- [Rep. Torres — GovTrack Profile (CA District 35)](https://www.govtrack.us/congress/members/CA/35)
- [California Senate District Mapping — District 35](https://sdmg.senate.ca.gov/committeehome/2025-congressional-districts/congressional-district-35-2025)
""")
