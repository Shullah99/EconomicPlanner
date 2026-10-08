import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import load_multipliers, get_solano_data, clean_dataframe, cleaned_data
from src.multiplier import employment_gap

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


#grab bls employment data and clean it up then pass it to pd
employment_data = clean_dataframe(cleaned_data(get_solano_data()))

tab1, tab2, tab3 = st.tabs(["Current Employment Status", "Investment Scenario Analysis", "Where to Invest"])

with tab1:
    #grab the row containing the series id, sort them, and grab the most recent one
    total_rows = employment_data[employment_data["series_id"]=="LAUCN060950000000003"]
    sorted_row = total_rows.sort_values(by="date", ascending=False)
    current_unemployment_rate = sorted_row["value"].dropna().iloc[0]
    #calculate employment rate by subtracting unemployment from 100
    current_employment_rate = 100 - current_unemployment_rate


    #labor force size
    labor_rows = employment_data[employment_data["series_id"]=="LAUCN060950000000006"]
    sorted_labor_row = labor_rows.sort_values(by="date", ascending=False)
    current_labor_size = sorted_labor_row["value"].dropna().iloc[0]
    
    employ_gap = employment_gap(current_employment_rate, current_labor_size, 0, 0)

    #guage for employment
    figure = go.Figure(go.Indicator(
    mode="gauge+number",
    value=current_employment_rate,
    title={"text": "Most Employment Rate (%)"},
    gauge={"axis": {"range": [0, 100]}}
    ))
    st.plotly_chart(figure)


    #key metrics for labor size
    column1, column2, column3 = st.columns(3)

    with column1:
        st.metric("Current Unemployment Rate", f"{current_unemployment_rate:.1f}%")

    with column2:
        st.metric("Workers Needed for Full Employment", f"{employ_gap[1]:,.0f}")

    with column3:
        st.metric("Consumption Capacity", f"{employ_gap[2]:.1f}%")
    