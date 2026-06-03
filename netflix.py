import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Title
st.title("🎬 Netflix Content Intelligence Dashboard")

# Load Data
df = pd.read_csv("netflix_titles.csv")

# Data Cleaning
df['country'] = df['country'].fillna("Unknown")
df['director'] = df['director'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Unknown")

df['date_added'] = pd.to_datetime(
    df['date_added'],
    errors='coerce'
)

df['year_added'] = df['date_added'].dt.year

# Sidebar Filters
st.sidebar.header("Filters")

content_type = st.sidebar.multiselect(
    "Content Type",
    df['type'].unique(),
    default=df['type'].unique()
)

country = st.sidebar.multiselect(
    "Country",
    sorted(df['country'].unique()),
    default=sorted(df['country'].unique())
)

filtered_df = df[
    (df['type'].isin(content_type)) &
    (df['country'].isin(country))
]

# KPIs
total_titles = filtered_df.shape[0]

movies = filtered_df[
    filtered_df['type']=="Movie"
].shape[0]

tvshows = filtered_df[
    filtered_df['type']=="TV Show"
].shape[0]

countries = filtered_df['country'].nunique()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", tvshows)
col4.metric("Countries", countries)

st.divider()

# Movies vs TV Shows
col1,col2 = st.columns(2)

with col1:

    type_count = filtered_df['type'].value_counts()

    fig = px.pie(
        values=type_count.values,
        names=type_count.index,
        title="Movies vs TV Shows"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    rating_count = filtered_df['rating'].value_counts().head(10)

    fig = px.bar(
        x=rating_count.index,
        y=rating_count.values,
        title="Ratings Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Content Added Over Time

st.subheader("Content Added Over Time")

yearly = filtered_df['year_added'].value_counts().sort_index()

fig = px.line(
    x=yearly.index,
    y=yearly.values,
    markers=True,
    title="Netflix Growth Over Years"
)

st.plotly_chart(fig, use_container_width=True)

# Top Countries

st.subheader("Top Countries")

country_count = (
    filtered_df['country']
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=country_count.values,
    y=country_count.index,
    orientation='h',
    title="Top 10 Countries"
)

st.plotly_chart(fig, use_container_width=True)

# Top Genres

st.subheader("Top Genres")

genres = (
    filtered_df['listed_in']
    .str.split(", ")
    .explode()
)

genre_count = genres.value_counts().head(10)

fig = px.bar(
    x=genre_count.index,
    y=genre_count.values,
    title="Top Genres"
)

st.plotly_chart(fig, use_container_width=True)

# Top Directors

st.subheader("Top Directors")

director_count = (
    filtered_df['director']
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=director_count.values,
    y=director_count.index,
    orientation='h',
    title="Top Directors"
)

st.plotly_chart(fig, use_container_width=True)

# Raw Data

with st.expander("View Dataset"):
    st.dataframe(filtered_df)