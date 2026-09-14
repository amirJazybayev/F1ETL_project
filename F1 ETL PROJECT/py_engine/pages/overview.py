import streamlit as st
import plotly.express as px
from db_connection import get_circuit_races, get_drivers_race, get_drivers_final, get_constructors_final

def render():
    st.title("📊 F1 dataset overview")

    # --- Load data ---
    circuit_races   = get_circuit_races()
    drivers_race    = get_drivers_race()
    drivers_final   = get_drivers_final()
    constructors    = get_constructors_final()

    #visual 1: KPI summary cards 
    st.subheader("Key Statistics")

    total_races       = circuit_races['raceid'].nunique()
    total_drivers     = drivers_final['driver_id'].nunique()
    total_constructors = constructors['constructor_id'].nunique()
    avg_points        = drivers_race['points'].mean()
    total_finishes    = (drivers_race['status'] == 'Finished').sum()
    dnf_rate          = (drivers_race['status'] != 'Finished').mean() * 100

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Races",        f"{total_races:,}")
    col2.metric("Unique Drivers",     f"{total_drivers:,}")
    col3.metric("Constructors",       f"{total_constructors:,}")
    col4.metric("Avg Points / Result",f"{avg_points:.2f}")
    col5.metric("Race Finishes",      f"{total_finishes:,}")
    col6.metric("DNF Rate",           f"{dnf_rate:.1f}%")

    st.divider()

    #visual 2: races per year (time-based line chart)
    st.subheader("Number of Races Per Season (Time-Based)")

    races_per_year = (
        circuit_races.groupby('year')['raceid']
        .count()
        .reset_index()
        .rename(columns={'raceid': 'race_count'})
    )

    fig = px.line(
        races_per_year,
        x='year',
        y='race_count',
        title='Number of F1 Races Per Season (1950–2022)',
        labels={'year': 'Season', 'race_count': 'Number of Races'},
        markers=True
    )
    fig.update_traces(line_color='#e10600', marker_color='#e10600')
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)