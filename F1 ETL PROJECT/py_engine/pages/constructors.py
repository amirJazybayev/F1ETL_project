import streamlit as st
import plotly.express as px
from db_connection import get_constructors_final, get_constructor_races, get_circuit_races, get_regs_eras

def render():
    st.title("🔩 Constructor Analysis")

    constructors     = get_constructors_final()
    constructor_races = get_constructor_races()
    circuit_races    = get_circuit_races()
    regs_eras        = get_regs_eras()

    #visual 6: top 15 constructors by all-time wins
    st.subheader("Top 15 Constructors by All-Time Wins")

    top_teams = (
        constructor_races
        .merge(constructors[['constructor_id', 'constructor_name']], on='constructor_id')
        .groupby('constructor_name')['wins']
        .max()
        .reset_index()
        .nlargest(15, 'wins')
    )

    fig6 = px.bar(
        top_teams,
        x='constructor_name',
        y='wins',
        title='Top 15 Constructors by All-Time Wins',
        labels={'constructor_name': 'Constructor', 'wins': 'Wins'},
        color='wins',
        color_continuous_scale='Reds'
    )
    fig6.update_layout(xaxis_tickangle=-35, coloraxis_showscale=False)
    st.plotly_chart(fig6, use_container_width=True)

    st.divider()

        #visual 7: highest scoring constructor every 5 years
    st.subheader("Highest Scoring Constructor Every 5 Years")

    # join year into constructor_races
    cr_year = constructor_races.merge(
        circuit_races[['raceid', 'year']],
        left_on='race_id', right_on='raceid'
    )

    cr_year['period_start'] = (cr_year['year'] // 5) * 5
    cr_year['period_label'] = (
        cr_year['period_start'].astype(str) + '–' +
        (cr_year['period_start'] + 4).astype(str)
    )

    period_pts = (
        cr_year.groupby(['period_label', 'period_start', 'constructor_id'])['constructor_points']
        .max()
        .reset_index()
    )

    top_per_period = (
        period_pts.loc[
            period_pts.groupby('period_label')['constructor_points'].idxmax()
        ]
        .merge(constructors[['constructor_id', 'constructor_name']], on='constructor_id')
        .sort_values('period_start')
    )

    fig7 = px.bar(
        top_per_period,
        x='period_label',
        y='constructor_points',
        color='constructor_name',
        title='Highest Scoring Constructor Every 5 Years',
        labels={
            'period_label':      '5-Year Period',
            'constructor_points': 'Points (Season Peak)',
            'constructor_name':  'Constructor'
        },
        text='constructor_name'
    )
    fig7.update_traces(textposition='outside')
    fig7.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,        
        hovermode='x unified'
    )
    st.plotly_chart(fig7, use_container_width=True)