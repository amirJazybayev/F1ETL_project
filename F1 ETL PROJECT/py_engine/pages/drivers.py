import streamlit as st
import plotly.express as px
from db_connection import get_drivers_final, get_drivers_race, get_driver_grid_final

def render():
    st.title("🧑‍🏎️ Driver Analysis")

    drivers_final    = get_drivers_final()
    drivers_race     = get_drivers_race()
    driver_grid      = get_driver_grid_final()

    #visual 3: top drivers by total championship points 
    st.subheader("Top 20 Drivers by All-Time Championship Points In A Single Season")

    top_drivers_pts = (
        driver_grid.groupby('driver_id')['points']
        .max()
        .reset_index()
        .merge(
            drivers_final[['driver_id', 'driver_firstname', 'driver_lastname']],
            on='driver_id'
        )
    )
    top_drivers_pts['driver_name'] = (
        top_drivers_pts['driver_firstname'] + ' ' + top_drivers_pts['driver_lastname']
    )
    top_drivers_pts = top_drivers_pts.nlargest(20, 'points')

    fig3 = px.bar(
        top_drivers_pts,
        x='driver_name',
        y='points',
        title='Top 20 Drivers by All-Time Championship Points',
        labels={'driver_name': 'Driver', 'points': 'Points'},
        color='points',
        color_continuous_scale='Reds'
    )
    fig3.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    #visual 4: driver nationality distribution
    st.subheader("Top 15 Driver Nationalities in F1 History")

    nationality_counts = (
        drivers_final['driver_nationality']
        .value_counts()
        .head(15)
        .reset_index()
    )
    nationality_counts.columns = ['nationality', 'count']

    fig4 = px.bar(
        nationality_counts,
        x='count',
        y='nationality',
        orientation='h',
        title='Top 15 Driver Nationalities in F1 History',
        labels={'count': 'Number of Drivers', 'nationality': ''},
        color='count',
        color_continuous_scale='Blues'
    )
    fig4.update_layout(coloraxis_showscale=False, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    #visual 5: grid position vs. final position scatter
    st.subheader("Does Grid Position Predict Race Result?")

    scatter_df = drivers_race[
        (drivers_race['start_position'] > 0) &
        (drivers_race['final_position'] > 0) &
        (drivers_race['final_position'] <= 20)
    ].copy()

    fig5 = px.scatter(
        scatter_df.sample(min(5000, len(scatter_df)), random_state=42),
        x='start_position',
        y='final_position',
        opacity=0.25,
        title='Grid Position vs. Final Race Position',
        labels={
            'start_position': 'Starting Grid Position',
            'final_position': 'Final Position'
        },
        color_discrete_sequence=['#e10600'],
        trendline='ols'
    )
    fig5.update_layout(hovermode='closest')
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("⚠️ This chart requires `statsmodels` for trendline: `pip install statsmodels`")