import streamlit as st
import pandas as pd
from src.data_loader import load_multipliers

#title
st.title("Solano County Economic Scenario Planner")

#load in multipliers and convert the sector name column in a list
multiplier_df = load_multipliers()
sector_list = multiplier_df["sector_name"].tolist()

#select sector sidebars
select_sector = st.sidebar.selectbox("Select Industry Sector", sector_list)

#direct job change sidebar set with in increment of 10
direct_job_change = st.sidebar.number_input("Change in Direct Jobs", value=0, step=10)

#radio sidebar that chooses between 2 types of multipliers
mult_type = st.sidebar.radio("Multiplier Type", ["type1", "type2"])

#timeline sidebar
timeframe = st.sidebar.slider("Timeframe (Years)", min_value=1, max_value=20, value=5)