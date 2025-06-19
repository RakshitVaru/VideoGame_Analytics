# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import plotly.express as px
# Write directly to the app
st.title(f":video_game: Video Game Sales Dashboard :balloon: ")
st.write(
  """**This webpage is hosted on Snowflake :snowflake: and coded in Python using Streamlit and Pandas.**
  """
)

# Get the current credentials
session = get_active_session()

df = session.table("GAME_SALES")
pandas_df = df.to_pandas()


genres = pandas_df['GENRE'].dropna().unique()
platforms = pandas_df['PLATFORM'].dropna().unique()
years = pandas_df['YEAR_OF_RELEASE'].dropna().unique()

genre = st.selectbox(":video_game: Genre", ["All"] + list(genres))
platform = st.selectbox(":joystick: Platform", ["All"] + list(platforms))
year = st.selectbox(":calendar: Year", ["All"] + sorted(list(set(years))))

filtered_df = pandas_df.copy()
if genre != "All":
    filtered_df = filtered_df[filtered_df["GENRE"] == genre]
if platform != "All":
    filtered_df = filtered_df[filtered_df["PLATFORM"] == platform]
if year != "All":
    filtered_df = filtered_df[filtered_df["YEAR_OF_RELEASE"] == year]



st.subheader(":abacus: Game Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Games", len(filtered_df))
col2.metric("Avg Critic Score", f"{filtered_df['CRITIC_SCORE'].mean():.2f}")
col3.metric("Total Global Sales (M)", f"{filtered_df['GLOBAL_SALES'].sum():,.2f}")

st.subheader(":dart: Sales by Genre")
genre_sales = (
    filtered_df.groupby("GENRE")["GLOBAL_SALES"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(genre_sales)

st.subheader(":earth_africa: Sales by Region")
region_sales = filtered_df[["NA_SALES", "EU_SALES", "JP_SALES", "OTHER_SALES"]].sum()
st.bar_chart(region_sales)

st.subheader(":chart_with_upwards_trend: Score vs. Sales")
scatter_df = filtered_df[["CRITIC_SCORE", "GLOBAL_SALES"]].dropna()
st.scatter_chart(scatter_df)




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

