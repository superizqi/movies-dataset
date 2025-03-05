import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px


# Show the page title and description.
st.set_page_config(page_title="YouTube Views Tracker", page_icon="🎬")
st.title("🎬 YouTube Views Tracker")
st.markdown("""
    Ever wondered how your favorite YouTube videos perform over time? This dashboard tracks view counts, updated every **2 minutes**! Select a video below and explore the trends! 🚀🎬  
""")


# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query("""
                SELECT 
                    data_created_at, 
                    title, 
                    channel_name, 
                    views_count, 
                    likes_count, 
                    comments_count, 
                    upload_date,
                    url
                FROM raw_youtube_data
                """, ttl="10m")

# Dropdown for Title Selection
unique_titles = df["title"].unique()
selected_title = st.selectbox("Select a Title", unique_titles)

# Filter Data based on selected Title
filtered_df = df[df["title"] == selected_title]



with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Views Over Time")
        idvid = str(df[df["title"] == selected_title]['url'].iloc[0]).split("v=")[1]
        video_url = f'https://www.youtube.com/embed/{idvid}'

        st.markdown(
            f"""
            <iframe width="320" height="180" src="{video_url}" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("❤️ Video")
        fig1 = px.line(filtered_df, x="data_created_at", y="views_count",
                    title=f"Views Count Over Time for {selected_title}", height=180)
        
        # Reduce margins, font sizes, and remove legend to fit small height
        fig1.update_layout(
            margin=dict(l=0, r=0, t=20, b=20),  # Reduce padding
            font=dict(size=10),  # Smaller font
            title=dict(font=dict(size=12)),  # Smaller title
            xaxis=dict(title=None, tickfont=dict(size=8)),  # Smaller x-axis
            yaxis=dict(title=None, tickfont=dict(size=8)),  # Smaller y-axis
            legend=dict(font=dict(size=8), orientation="h")  # Horizontal legend
        )
        st.plotly_chart(fig1, use_container_width=True)



# Display the selected video
# st.video(df[df["title"] == selected_title]['url'].iloc[0])

### --- DIM TABLES ---
# dim_video
dim_video = df[['title', 'channel_name', 'upload_date', 'url']].drop_duplicates().reset_index(drop=True)
dim_video.insert(0, "video_id", range(1, len(dim_video) + 1))

# Ensure data_created_at is in datetime format
df["data_created_at"] = pd.to_datetime(df["data_created_at"])

# dim_date
dim_date = df[['data_created_at']].drop_duplicates().reset_index(drop=True)
dim_date['year'] = dim_date['data_created_at'].dt.year
dim_date['month'] = dim_date['data_created_at'].dt.month
dim_date['day'] = dim_date['data_created_at'].dt.day
dim_date.insert(0, "date_id", range(1, len(dim_date) + 1))

### --- FACT TABLE ---
fact_video_metrics = df.merge(dim_video, on=['title', 'channel_name', 'upload_date', 'url'], how='left') \
                       .merge(dim_date, on='data_created_at', how='left') \
                       [['video_id', 'date_id', 'views_count', 'likes_count', 'comments_count']]

### --- MART TABLE ---
mart_video_summary = fact_video_metrics.groupby("video_id").agg(
    total_views=pd.NamedAgg(column="views_count", aggfunc="max"),
    total_likes=pd.NamedAgg(column="likes_count", aggfunc="max"),
    total_comments=pd.NamedAgg(column="comments_count", aggfunc="max"),
).reset_index()

### --- STREAMLIT UI ---
# st.title("📊 YouTube Video Data Warehouse")

st.data_editor(
    df,
    column_config={
        "title": st.column_config.TextColumn(width="small"),
        "channel_name": st.column_config.TextColumn(width="medium"),
    },
    hide_index=True
)

# Row 1: Dim Tables
st.subheader("📁 Dimension Tables")
st.write("🔹 **dim_video**")
st.dataframe(dim_video)

st.write("🔹 **dim_date**")
st.dataframe(dim_date)

st.subheader("📊 Fact & Mart Tables")
st.write("📌 **fact_video_metrics**")
st.dataframe(fact_video_metrics)

st.write("📈 **mart_video_summary**")
st.dataframe(mart_video_summary)

# Row 2: Fact & Mart Tables

# row2_col1, row2_col2 = st.columns(2)
# with row2_col1:
#     st.write("📌 **fact_video_metrics**")
#     st.dataframe(fact_video_metrics)

# with row2_col2:


# Row 3: Visualizations
# st.subheader("📊 Visualizing YouTube Data")

# # Line Chart (Views over Time)
# fig_line = px.line(fact_video_metrics.merge(dim_date, on="date_id"),
#                    x="data_created_at", y="views_count", color="video_id",
#                    title="📈 Views Over Time")
# st.plotly_chart(fig_line, use_container_width=True)

# # Bar Chart (Total Views by Video)
# fig_bar = px.bar(mart_video_summary.merge(dim_video, on="video_id"),
#                  x="title", y="total_views", title="📊 Total Views by Video")
# st.plotly_chart(fig_bar, use_container_width=True)


# # 🔹 Row 1: 2 Columns
# with st.container():
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("📊 Views Over Time")
#         # st.markdown('<div class="custom-container">', unsafe_allow_html=True)
#         # Plotly Line Chart
#         fig1 = px.line(filtered_df, x="data_created_at", y="views_count",
#                     title=f"Views Count Over Time for {selected_title}")
#        # Display Chart
#         st.plotly_chart(fig1, use_container_width=True)
#         # st.markdown('</div>', unsafe_allow_html=True)

#     with col2:
#         st.subheader("❤️ Video")
#         # st.markdown('<div class="custom-container">', unsafe_allow_html=True)
#         st.video(df[df["title"] == selected_title]['url'].iloc[0])
#         # st.markdown('</div>', unsafe_allow_html=True)

# # 🔹 Row 2: 3 Columns
# with st.container():
#     col3, col4 = st.columns(2)

#     with col3:
#         st.subheader("💬 Raw Data")
#         # Display the data as a table using `st.dataframe`.
#         st.dataframe(
#         df[df["title"] == selected_title],
#         use_container_width=True
#         )

#     with col4:
#         st.subheader("🔁 Raw Data")
#         st.dataframe(
#         df[df["title"] == selected_title],
#         use_container_width=True
#         )


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
# st.dataframe(
#     df,
#     use_container_width=True,
#     column_config={"year": st.column_config.TextColumn("Year")},
# )


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
