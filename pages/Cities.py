import streamlit as st

import utils.cities_data as cdt


def make_sidebar(df):
    st.sidebar.markdown("## Filters")

    countries = st.sidebar.multiselect(
        "Choose the countries you want to view the information",
        df.loc[:, "country"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    return list(countries)


def main():
    st.set_page_config(page_title="Cities", page_icon="🏙️", layout="wide")

    df = cdt.read_processed_data()

    countries = make_sidebar(df)

    st.markdown("# :cityscape: Cities Perspective")

    fig = cdt.top_cities_restaurants(countries)

    st.plotly_chart(fig, use_container_width=True)

    best, worst = st.columns(2)

    with best:
        fig = cdt.top_best_restaurants(countries)

        st.plotly_chart(fig, use_container_width=True)

    with worst:
        fig = cdt.top_worst_restaurants(countries)

        st.plotly_chart(fig, use_container_width=True)

    fig = cdt.most_cuisines(countries)

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()