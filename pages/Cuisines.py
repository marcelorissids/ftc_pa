import streamlit as st

import utils.cuisines_data as cdt


def make_sidebar(df):
    st.sidebar.markdown("## Filters")

    countries = st.sidebar.multiselect(
        "Choose the Countries you want to view information",
        df.loc[:, "country"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    top_n = st.sidebar.slider(
        "Select the number of Restaurants you want to view", 1, 20, 10
    )

    cuisines = st.sidebar.multiselect(
        "Choose Types of Cuisine",
        df.loc[:, "cuisines"].unique().tolist(),
        default=[
            "Home-made",
            "BBQ",
            "Japanese",
            "Brazilian",
            "Arabian",
            "American",
            "Italian",
        ],
    )

    return list(countries), top_n, list(cuisines)


def main():
    st.set_page_config(page_title="Cuisines", page_icon="🍽️", layout="wide")

    df = cdt.read_processed_data()

    countries, top_n, cuisines = make_sidebar(df)

    st.markdown("# :knife_fork_plate: View Types of Cuisines")

    df_restaurants = cdt.top_restaurants(countries, cuisines, top_n)

    st.markdown(f"## Best Restaurants of the Main Culinary Types")

    cdt.write_metrics()

    st.markdown(f"## Top {top_n} Restaurants")

    st.dataframe(df_restaurants)

    best, worst = st.columns(2)

    with best:
        fig = cdt.top_best_cuisines(countries, top_n)

        st.plotly_chart(fig, use_container_width=True)

    with worst:
        fig = cdt.top_worst_cuisines(countries, top_n)

        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()