from py_compile import main
import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image 
from streamlit_folium import folium_static

from utils import general_data as gd
from utils.process_data import process_data 

raw_data_path = f'./data/raw/zomato.csv'

def create_sidebar(df):
    image_path = "./img/"
    image = Image.open(image_path + "logo.png")

    col1, col2 = st.sidebar.columns([1, 4], gap="small")
    col1.image(image, width=35)
    col2.markdown("# Zero Hunger")

    st.sidebar.markdown("## Filters")

    countries = st.sidebar.multiselect(
        "Choose the countries you want to view the restaurants",
        df.loc[:, "country"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    st.sidebar.markdown("### Treated Data")

    processed_data = pd.read_csv("./data/processed/data.csv")

    st.sidebar.download_button(
        label="Download",
        data=processed_data.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )

    return list(countries)

def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)

    def main():

        df = process_data(raw_data_path)

        st.set_page_config(page_title="Home", page_icon="📌", layout="wide")

        selected_countries = create_sidebar(df)

        st.markdown("# Zero Hunger!")

        st.markdown("## The Best Place to find your new favorite restaurant!")

        st.markdown("### We have the following brands within our platform:")

        restaurants, countries, cities, ratings, cuisines = st.columns(5)

        restaurants.metric(
            "Registered Restaurants",
            gd.qty_restaurants(df),
        )

        countries.metric(
            "Registered Countries",
            gd.qty_countries(df),
        )

        cities.metric(
            "Registered Cities",
            gd.qty_cities(df),
        )

        ratings.metric(
            "Reviews Made on the Platform",
            f"{gd.qty_ratings(df):,}".replace(",", "."),
        )

        cuisines.metric(
            f"Types of Cuisine Offered",
            f"{gd.qty_cuisines(df):,}",
        )

        map_df = df.loc[df["country"].isin(selected_countries), :]

        create_map(map_df)

        return None


if __name__ == "__main__":
    main()