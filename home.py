import streamlit as st
st.set_page_config(page_title="Chinmayee Phirke", layout="wide")

st.title("Hi, I'm Chinmayee Phirke")
st.write("My work lies at the intersection of economics and data science.
          I love using logic and math to solve real-world problems and I strive to understand how data and economic choices can improve systems and make a meaningful impact on our environment and communities. 
          Through my school classes and independent projects, I've built data tools that turn complicated information into clear, useful solutions.
        ")

st.subheader("My Projects")
col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/1_Transit_Research.py",
        label="**Public Transit Analysis** — is transit access fair across the district for school students?",
        
    )

with col2:
    st.page_link(
        "pages/2_Hydrogen_EV_TCO.py",
        label="**Hydrogen vs. Battery Buses** — which is cheaper in the long run?",
        
    )
    

st.divider()
st.subheader("Connect with me")
st.write("Connect with me on [LinkedIn](https://www.linkedin.com/in/chinmayee-phirke-4954ab39a/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BL56aXZ58RVqZh7HU8cposA%3D%3D)")
