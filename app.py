import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import load_multipliers, get_solano_data, clean_dataframe, cleaned_data
from src.multiplier import employment_gap, mult_effect, growth_timeline, ranked_sectors

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
type_labels = {"type1": "Type I",
                   "type2": "Type II"}
mult_type = st.sidebar.radio("Multiplier Type", ["type1", "type2"], format_func=type_labels.get)


avg_wage = st.sidebar.number_input("Average Annual Wage ($)", value=62000, step=1000)

#grab bls employment data and clean it up then pass it to pd
@st.cache_data(ttl=86400)
def load_employment_data():
    return clean_dataframe(cleaned_data(get_solano_data()))

try:
    employment_data = load_employment_data()

except RuntimeError as error:
    st.error("Live employment data is temporarily unavailable. Please try again in a few minutes.")
    st.caption(str(error))
    st.stop()


section = st.radio(
    "Section",
    ["Current Employment Status", "Investment Scenario Analysis", "Where to Invest"],
    horizontal=True,
    label_visibility="collapsed",
)

#tab 1
if section == "Current Employment Status":
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

    # latest month that has Solano data, so state and county compare the same month
    latest_date = sorted_row.dropna(subset=["value"])["date"].iloc[0]

    # California unemployment rate for that same month, state employment rate
    state_rows = employment_data[
        (employment_data["series_id"] == "LAUST060000000000003")
        & (employment_data["date"] == latest_date)
    ]
    state_employment_rate = 100 - state_rows["value"].iloc[0]

    # employment gap, now with the real wage and state rate
    employ_gap = employment_gap(current_employment_rate, current_labor_size, avg_wage, state_employment_rate)

    #guage for employment
    figure = go.Figure(go.Indicator(
    mode="gauge+number",
    value=current_employment_rate,
    title={"text": "Portion of the Labor Force Employed (%)"},
    gauge={"axis": {"range": [85, 100]}}
    ))
    st.plotly_chart(figure)
    st.caption(f"Data as of {latest_date:%B %Y}. Shows the share of the labor force that is employed (100 minus the unemployment rate). The labor force counts only people working or actively looking for work.")


    #key metrics for labor size
    column1, column2, column3 = st.columns(3)

    with column1:
        st.metric("Current Unemployment Rate", f"{current_unemployment_rate:.1f}%")

    with column2:
        st.metric("Workers Needed for Full Employment", f"{employ_gap[1]:,.0f}")

    with column3:
        st.metric("Consumption Capacity", f"{employ_gap[2]:.1f}%")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Employment Gap vs. California(Basis Points)", f"{employ_gap[4]:.1f} pts")

    with col5:
        st.metric("Estimated Annual Lost Wages", f"${employ_gap[3]/1e6:,.1f}M")

#tab 2
if section == "Investment Scenario Analysis":

    st.caption("Multipliers are national industry averages (EPI, 2019), not Solano-specific, so results are estimates.")

    if select_sector == "Government / public administration":
        st.caption("The Government multiplier comes from a different, state-level source and is approximate.")

    # growth timeline
    timeline = growth_timeline(select_sector)
    min_years = timeline["min_years"].iloc[0]
    max_years = timeline["max_years"].iloc[0]
    st.caption(f"Typical time to full impact: {min_years:g} to {max_years:g} years (illustrative estimate).")

    
    # Government has no Type I multiplier, so fall back to Type II
    effective_type = mult_type
    if select_sector == "Government / public administration" and mult_type == "type1":
        effective_type = "type2"
        st.info("Type I isn't available for Government. Showing Type II instead.")

    total_jobs, indirect_jobs, direct_wages, indirect_wages, total_wages = mult_effect(
        select_sector, direct_job_change, effective_type, avg_wage
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Jobs Impact", f"{total_jobs:,.0f}")

    with col2:
        st.metric("Indirect Jobs (Ripple)", f"{indirect_jobs:,.0f}")

    with col3:
        st.metric("Total Wage Impact", f"${total_wages/1e6:,.1f}M")

    fig2 = go.Figure(go.Bar(x=["Direct", "Indirect", "Total"], y=[direct_job_change, indirect_jobs, total_jobs]))
    fig2.update_layout(title="Job Impact by Stage", yaxis_title="Jobs")
    st.plotly_chart(fig2)

#tab 3
if section == "Where to Invest":
    ranked_df, top_5, bottom_5 = ranked_sectors(mult_type)

    if mult_type == "type1":
        mult_column = "type1_mult"
    else:
        mult_column = "type2_mult"

    ranked_df = ranked_df.dropna(subset=[mult_column])


    colors = ["#1f77b4" if i < 3 else "#c7c7c7" for i in range(len(ranked_df))]
    fig3 = go.Figure(go.Bar(x=ranked_df[mult_column], y=ranked_df["sector_name"], orientation="h", marker_color=colors))
    fig3.update_layout(title="Ranked Sectors By Multiplier", xaxis_title="Total Jobs Per Direct Job", yaxis=dict(autorange="reversed"), height=700)
    st.plotly_chart(fig3)

    top_sector = ranked_df["sector_name"].iloc[0]
    top_value = ranked_df[mult_column].iloc[0]
    st.write(f"**{top_sector}** has the highest ripple effect per direct job ({top_value:.1f} total jobs for every direct job), based on national industry averages.")
    st.caption("This ranks ripple effect per direct job, not return per dollar invested, and it doesn't mean Solano has a large presence in that industry.")