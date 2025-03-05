import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px

# import streamlit as st

# conn = st.connection('pets_db', type='sql')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM raw_youtube_data;', ttl="10m")

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🎬")
st.title("🎬 Movies dataset")
st.write(
    """
    This app visualizes data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    It shows which movie genre performed best at the box office over the years. Just 
    click on the widgets below to explore!  
    """
)

# Streamlit UI
# st.title("Views Count Over Time by Title")

# Dropdown for Title Selection
unique_titles = df["title"].unique()
selected_title = st.selectbox("Select a Title", unique_titles)

# Filter Data based on selected Title
filtered_df = df[df["title"] == selected_title]

# Plotly Line Chart
fig = px.line(filtered_df, x="data_created_at", y="views_count",
              title=f"Views Count Over Time for {selected_title}")

# Display Chart
st.plotly_chart(fig)

# st.title("Select a YouTube Video")

# Dictionary of video titles and their corresponding YouTube links
# videos = {
#     "Video 1": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
#     "Video 2": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
#     "Video 3": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"
# }

# # Dropdown to select video
# selected_video = st.selectbox("Choose a video:", list(videos.keys()))

# # Display the selected video
# st.video(videos[selected_video])


# import streamlit as st
# import pandas as pd
# import psycopg2
# from sqlalchemy import create_engine

# secret_db = st.secrets["postgres"]["SECRET_KEY"]

# # Function to get data
# @st.cache_data
# def get_data(query):
#     # Using SQLAlchemy
#     engine = create_engine(secret_db)
#     with engine.connect() as conn:
#         df = pd.read_sql(query, conn)
#     return df

# # Streamlit UI
# st.title("PostgreSQL Data in Streamlit")

# query = "SELECT * FROM raw_test LIMIT 10"
# df = get_data(query)

# st.write("### Data from PostgreSQL")
# st.dataframe(df)



# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/movies_genres_summary.csv")
#     return df


# df = load_data()

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)


# Show a multiselect widget with the genres using `st.multiselect`.
# genres = st.multiselect(
#     "Genres",
#     df.genre.unique(),
#     ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
# )

# Show a slider widget with the years using `st.slider`.
# years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
# df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
# df_reshaped = df_filtered.pivot_table(
#     index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
# )
# df_reshaped = df_reshaped.sort_values(by="year", ascending=False)



# Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("year:N", title="Year"),
#         y=alt.Y("gross:Q", title="Gross earnings ($)"),
#         color="genre:N",
#     )
#     .properties(height=320)
# )
# st.altair_chart(chart, use_container_width=True)
