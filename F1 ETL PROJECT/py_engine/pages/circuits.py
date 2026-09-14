# pages/circuits.py
import streamlit as st
import plotly.express as px
from db_connection import get_circuits_final, get_circuit_races, get_drivers_race, get_regs_eras

def render():
    st.title("🛣️ Circuit & Regulations Era Analysis")

    circuits_final = get_circuits_final()
    circuit_races  = get_circuit_races()
    drivers_race   = get_drivers_race()
    regs_eras      = get_regs_eras()

    #visual 8: races hosted per country choropleth map
    st.subheader("Number of F1 Races Hosted by Country")

    races_per_country = (
        circuit_races
        .merge(circuits_final[['circuit_reference', 'circuit_country']], on='circuit_reference')
        .groupby('circuit_country')['raceid']
        .count()
        .reset_index()
        .rename(columns={'raceid': 'total_races'})
    )

    fig8 = px.choropleth(
        races_per_country,
        locations='circuit_country',
        locationmode='country names',
        color='total_races',
        title='Number of F1 Races Hosted by Country',
        color_continuous_scale='YlOrRd',
        labels={'total_races': 'Races Hosted'}
    )
    st.plotly_chart(fig8, use_container_width=True)

    st.divider()

    #visual 9: fastest lap speed vs. circuit altitude
    st.subheader("Fastest Lap Speed vs. Circuit Altitude")

    speed_alt = (
        drivers_race[drivers_race['fastest_lap_speed'] > 0]
        [['race_id', 'fastest_lap_speed']]
        .merge(circuit_races[['raceid', 'circuit_reference']], left_on='race_id', right_on='raceid')
        .merge(circuits_final[['circuit_reference', 'circuit_alt', 'circuit_name']], on='circuit_reference')
    )

    avg_speed_alt = (
        speed_alt.groupby(['circuit_name', 'circuit_alt'])['fastest_lap_speed']
        .mean()
        .reset_index()
        .rename(columns={'fastest_lap_speed': 'avg_fastest_speed'})
    )

    fig9 = px.scatter(
        avg_speed_alt,
        x='circuit_alt',
        y='avg_fastest_speed',
        hover_name='circuit_name',
        title='Average Fastest Lap Speed vs. Circuit Altitude',
        labels={
            'circuit_alt': 'Circuit Altitude (m)',
            'avg_fastest_speed': 'Avg Fastest Lap Speed (km/h)'
        },
        color='avg_fastest_speed',
        color_continuous_scale='Plasma',
        trendline='ols'
    )
    st.plotly_chart(fig9, use_container_width=True)
    st.caption("⚠️ Requires `statsmodels`: `pip install statsmodels`")

    st.divider()

    #visual 10: number of races per regulation era (stacked bar)
    st.subheader("Number of Races Per Regulation Era")

    def map_era(year):
        for _, row in regs_eras.iterrows():
            if row['start_year'] <= year <= row['end_year']:
                return row['era_name']
        return 'Other'

    era_races = circuit_races.copy()
    era_races['era'] = era_races['year'].apply(map_era)

    era_counts = (
        era_races.groupby(['era', 'year'])['raceid']
        .count()
        .reset_index()
        .rename(columns={'raceid': 'race_count'})
    )

    fig10 = px.bar(
        era_counts,
        x='year',
        y='race_count',
        color='era',
        title='Number of Races Per Season Coloured by Regulation Era',
        labels={'year': 'Season', 'race_count': 'Races', 'era': 'Era'},
        barmode='stack'
    )
    fig10.update_layout(hovermode='x unified', legend_title_text='Regulation Era')
    st.plotly_chart(fig10, use_container_width=True)