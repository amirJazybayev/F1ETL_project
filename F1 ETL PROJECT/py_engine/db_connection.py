import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:033VER$tappen@localhost:5432/formula1")

def load_table(table_name: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

def get_circuits_final():        
    return load_table("circuits_final")

def get_circuit_races():        
    return load_table("circuit_races")

def get_regs_eras():            
    return load_table("regs_eras")

def get_drivers_final():        
    return load_table("drivers_final")

def get_drivers_race():         
    return load_table("drivers_race")

def get_driver_grid_final():    
    return load_table("driver_grid_final")

def get_constructors_final():   
    return load_table("constructors_final")

def get_constructor_races():    
    return load_table("constructor_races")