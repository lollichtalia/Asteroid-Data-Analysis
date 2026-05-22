import streamlit as st
import pandas as pd
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Asteroid Data Analysis", layout="wide")

st.title("☄️ Asteroid Data Analysis")

df = pd.read_csv("data/neos.csv")

# Sidebar controls
st.sidebar.header("Filters")

hazard_option = st.sidebar.selectbox(
    "Hazard Status",
    ["All", "Hazardous", "Not Hazardous"]
)

min_diameter, max_diameter = st.sidebar.slider(
    "Max Diameter (km)",
    float(df["diameter_max_km"].min()),
    float(df["diameter_max_km"].max()),
    (float(df["diameter_max_km"].min()), float(df["diameter_max_km"].max()))
)

# Apply filters
filtered_df = df.copy()

if hazard_option == "Hazardous":
    filtered_df = filtered_df[filtered_df["hazardous"] == True]
elif hazard_option == "Not Hazardous":
    filtered_df = filtered_df[filtered_df["hazardous"] == False]

filtered_df = filtered_df[
    (filtered_df["diameter_max_km"] >= min_diameter) &
    (filtered_df["diameter_max_km"] <= max_diameter)
]

st.subheader("Dataset Overview")
st.write(f"Total Objects: {len(filtered_df)}")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Average Miss Distance (km)",
        round(filtered_df["miss_distance_km"].mean(), 2)
    )

with col2:
    st.metric(
        "Average Velocity (km/s)",
        round(filtered_df["velocity_km_s"].mean(), 2)
    )

st.subheader("Velocity vs Miss Distance")
st.scatter_chart(
    filtered_df[["miss_distance_km", "velocity_km_s"]]
)

st.subheader("Filtered Data")
st.dataframe(filtered_df)

# AI Insights
st.subheader("🧠 Ask the Data")

user_question = st.text_input("Ask a question about the asteroid data:")

if user_question:
    total_objs = len(filtered_df)
    unique_objs = filtered_df["id"].nunique()
    hazardous = filtered_df["hazardous"].sum()
    hazard_rate = filtered_df["hazardous"].mean() * 100

    haz = (
        filtered_df[filtered_df["hazardous"] == True]
        [["diameter_max_km", "velocity_km_s", "miss_distance_km"]]
        .mean()
    )

    nonhaz = (
        filtered_df[filtered_df["hazardous"] == False]
        [["diameter_max_km", "velocity_km_s", "miss_distance_km"]]
        .mean()
    )

    comparison = pd.DataFrame({
        "hazardous": haz,
        "non_hazardous": nonhaz
    })

    comparison_text = comparison.to_string()

    sample_data = filtered_df.head(10).to_dict(orient="records")

    prompt = f"""
    You are analyzing an asteroid dataset.

    Authoritative dataset metrics
    (do NOT recompute these from examples):

    Total observations: {total_objs}
    Unique asteroids: {unique_objs}
    Hazardous asteroids: {hazardous}
    Hazard percentage: {hazard_rate:.1f}%

    Hazard vs Non-Hazard Comparison:
    {comparison_text}

    Example observations only
    (do NOT infer totals from them):

    {sample_data}

    Question:
    {user_question}

    Answer using the authoritative metrics.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You analyze scientific datasets."},
                {"role": "user", "content": prompt}
            ]
        )  
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.warning("AI service is currently unavailable. Showing basic analysis instead.")

        # fallback answer
        st.write(f"Total asteroids: {len(filtered_df)}")
        st.write(f"Average diameter: {filtered_df['diameter_max_km'].mean():.2f} km")
        st.write(f"Average velocity: {filtered_df['velocity_km_s'].mean():.2f} km/s")