import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def read_processed_data():
    return pd.read_csv("./data/processed/data.csv")


def top_cities_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df["country"].isin(countries), ["restaurant_id", "country", "city"]]
        .groupby(["country", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(10),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country",
        title="Top 10 Cities with more Restaurants in the Database",
        labels={
            "city": "City",
            "restaurant_id": "Quantity Restaurants",
            "country": "Country",
        },
    )

    return fig


def top_best_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[
            (df["aggregate_rating"] >= 4) & (df["country"].isin(countries)),
            ["restaurant_id", "country", "city"],
        ]
        .groupby(["country", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country",
        title="Top 7 Cities with Restaurants - average rating above 4",
        labels={
            "city": "City",
            "restaurant_id": "Quantity Restaurants",
            "country": "Country",
        },
    )

    return fig


def top_worst_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[
            (df["aggregate_rating"] <= 2.5) & (df["country"].isin(countries)),
            ["restaurant_id", "country", "city"],
        ]
        .groupby(["country", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country",
        title="Top 7 Cities with Restaurants - average rating below 2.5",
        labels={
            "city": "City",
            "restaurant_id": "Quantity Restaurants",
            "country": "Country",
        },
    )

    return fig


def most_cuisines(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df["country"].isin(countries), ["cuisines", "country", "city"]]
        .groupby(["country", "city"])
        .nunique()
        .sort_values(["cuisines", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(10),
        x="city",
        y="cuisines",
        text="cuisines",
        color="country",
        title="Top 10 Cities with more restaurants with different types of cuisine",
        labels={
            "city": "City",
            "cuisines": "Number of Unique Culinary Types",
            "country": "Country",
        },
    )

    return fig