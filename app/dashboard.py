import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.snowflake_connector import connect_to_snowflake
import plotly.express as px
# Title
st.set_page_config(page_title="Game Sales Dashboard", layout="wide")
st.title("🎮 Video Game Sales Dashboard")

# Fetch data from Snowflake
@st.cache_data(ttl=600)
def load_data():
    conn = connect_to_snowflake()
    query = "SELECT * FROM game_sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# Filters
genres = df['GENRE'].dropna().unique()
platforms = df['PLATFORM'].dropna().unique()
years = df['YEAR_OF_RELEASE'].dropna().astype(int).sort_values().unique()

col1, col2, col3 = st.columns(3)
with col1:
    selected_genre = st.selectbox(":video_game: Genre", options=["All"] + list(genres))
with col2:
    selected_platform = st.selectbox(":joystick: Platform", options=["All"] + list(platforms))
with col3:
    selected_year = st.selectbox(":calendar: Year", options=["All"] + list(years))

# Apply filters
filtered_df = df.copy()
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["GENRE"] == selected_genre]
if selected_platform != "All":
    filtered_df = filtered_df[filtered_df["PLATFORM"] == selected_platform]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["YEAR_OF_RELEASE"] == selected_year]

# KPIs
st.subheader(":abacus: Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Games", len(filtered_df))
col2.metric("Avg Critic Score", f"{filtered_df['CRITIC_SCORE'].mean():.2f}")
col3.metric("Total Global Sales (M)", f"{filtered_df['GLOBAL_SALES'].sum():,.2f}")

# Charts
st.subheader(":dart: Sales by Genre")
top_genres = (
    filtered_df.groupby("GENRE")["GLOBAL_SALES"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(top_genres)

st.subheader(":earth_africa: Sales by Region")
region_sales = filtered_df[["NA_SALES", "EU_SALES", "JP_SALES", "OTHER_SALES"]].sum()
st.bar_chart(region_sales)

st.subheader(":chart_with_upwards_trend: Critic Score vs Global Sales")
st.scatter_chart(filtered_df[["CRITIC_SCORE", "GLOBAL_SALES"]].dropna())


st.subheader(":fire: Heatmap to show Correlation")

corr_matrix = filtered_df[[
    "NA_SALES", "EU_SALES", "JP_SALES", "OTHER_SALES",
    "GLOBAL_SALES", "CRITIC_SCORE", "USER_SCORE"
]].corr().round(2)

fig = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="blues",
    aspect="auto"
)
st.plotly_chart(fig)