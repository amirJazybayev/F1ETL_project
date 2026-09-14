import streamlit as st
import pandas as pd
from datetime import date
from db_connection import get_drivers_final, get_drivers_race, get_driver_grid_final, get_circuit_races

def render():
    st.title("🧑‍🏎️ Driver Profile")

    drivers_final  = get_drivers_final()
    drivers_race   = get_drivers_race()
    driver_grid    = get_driver_grid_final()
    circuit_races  = get_circuit_races()

    drivers_final['full_name'] = (
        drivers_final['driver_firstname'] + ' ' + drivers_final['driver_lastname']
    )
    sorted_drivers = drivers_final.sort_values('full_name')

    name_to_id = dict(zip(sorted_drivers['full_name'], sorted_drivers['driver_id']))

    selected_name = st.selectbox(
        "Select a Driver",
        options=list(name_to_id.keys()),   
        index=0
    )

    selected_id = name_to_id[selected_name]

    driver_row = drivers_final[drivers_final['driver_id'] == selected_id].iloc[0]

    dob = pd.to_datetime(driver_row['driver_dob'], errors='coerce')
    if pd.notna(dob):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        age_str = str(age)
    else:
        age_str = "N/A"

    dr_driver = drivers_race[drivers_race['driver_id'] == selected_id]

    races_entered = len(dr_driver)
    total_wins    = (dr_driver['final_position'] == 1).sum()
    podiums       = (dr_driver['final_position'].isin([1, 2, 3])).sum()

    if races_entered > 0:
        years_df = dr_driver[['race_id']].merge(
            circuit_races[['raceid', 'year']],
            left_on='race_id',
            right_on='raceid',
            how='left'
        )
        years = years_df['year'].dropna().astype(int)
        if not years.empty:
            first_year = years.min()
            last_year  = years.max()
            active_years = f"{first_year} – {last_year}"
            seasons_count = years.nunique()
        else:
            active_years  = "N/A"
            seasons_count = 0
    else:
        active_years  = "N/A"
        seasons_count = 0

    dg_driver = driver_grid[driver_grid['driver_id'] == selected_id]
    if not dg_driver.empty:

        career_wins_grid = dg_driver['wins'].max()
    else:
        career_wins_grid = 0

    display_wins = int(total_wins)

    st.divider()
    st.subheader(f"👤 {driver_row['driver_firstname']} {driver_row['driver_lastname']}")
    st.caption(f"🌍 Nationality: **{driver_row['driver_nationality']}**  |  🎂 DOB: **{dob.strftime('%B %d, %Y') if pd.notna(dob) else 'N/A'}**")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Age",          age_str)
    col2.metric("Races Entered", f"{races_entered:,}")
    col3.metric("Active Years",  active_years)
    col4.metric("Seasons",       f"{seasons_count}")

    st.write("")  

    col5, col6, col7 = st.columns(3)
    col5.metric("🏆 Total Wins",  f"{display_wins:,}")
    col6.metric("🥇🥈🥉 Podiums",  f"{podiums:,}")

    if races_entered > 0:
        podium_rate = (podiums / races_entered) * 100
        col7.metric("Podium Rate",  f"{podium_rate:.1f}%")
    else:
        col7.metric("Podium Rate",  "N/A")

    if not dg_driver.empty:
        st.divider()
        st.subheader("Points Per Season")

        pts_years = dg_driver.merge(
            circuit_races[['raceid', 'year']],
            left_on='race_id',
            right_on='raceid',
            how='left'
        ).dropna(subset=['year'])

        pts_years['year'] = pts_years['year'].astype(int)

        points_per_season = (
            pts_years.groupby('year')['points']
            .max()
            .reset_index()
            .rename(columns={'points': 'season_points'})
            .sort_values('year')
        )

        import plotly.express as px
        fig = px.bar(
            points_per_season,
            x='year',
            y='season_points',
            title=f"{driver_row['driver_firstname']} {driver_row['driver_lastname']} — Points Per Season",
            labels={'year': 'Season', 'season_points': 'Championship Points'},
            color='season_points',
            color_continuous_scale='Reds',
            text='season_points'
        )
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            coloraxis_showscale=False,
            xaxis=dict(tickmode='linear', dtick=1, tickangle=-45),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No championship standings data available for this driver.")