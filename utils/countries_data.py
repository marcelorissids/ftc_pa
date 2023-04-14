import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def read_processed_data():
    return pd.read_csv("./data/processed/data.csv")


def countries_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df["country"].isin(countries), ["restaurant_id", "country"]]
        .groupby("country")
        .count()
        .sort_values("restaurant_id", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="restaurant_id",
        text="restaurant_id",
        title="Number of Registered Restaurants by Country",
        labels={
            "country": "Countries",
            "restaurant_id": "Number of Restaurants",
        },
    )

    return fig


def countries_cities(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df["country"].isin(countries), ["city", "country"]]
        .groupby("country")
        .nunique()
        .sort_values("city", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="city",
        text="city",
        title="Number of Cities Registered by Country",
        labels={
            "country": "Countries",
            "city": "Number of Cities",
        },
    )

    return fig


def countries_mean_votes(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df["country"].isin(countries), ["votes", "country"]]
        .groupby("country")
        .mean()
        .sort_values("votes", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="votes",
        text="votes",
        text_auto=".2f",
        title="Average Ratings by Country",
        labels={
            "country": "Countries",
            "votes": "Number of Reviews",
        },
    )

    return fig


def countries_average_plate(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df["country"].isin(countries), ["average_cost_for_two", "country"]]
        .groupby("country")
        .median()
        .sort_values("average_cost_for_two", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="average_cost_for_two",
        text="average_cost_for_two",
        text_auto=".2f",
        title="Average Price of a dish for two people by Country",
        labels={
            "country": "Countries",
            "average_cost_for_two": "Plate price for two people",
        },
    )

    return fig