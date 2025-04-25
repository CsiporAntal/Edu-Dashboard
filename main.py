import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

# MongoDB connection
# 27017

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["edu_dashboard"]

# Page config
st.set_page_config(page_title="Education Dashboard", layout="wide")
# st.title("📈 Education Dashboard (MongoDB + Streamlit)")

# Sidebar - Select dataset type and year
st.sidebar.header("📁 Dataset Selection")

# Sidebar - Comparison options
st.sidebar.subheader("📊 Comparison Options")
compare_finals = st.sidebar.checkbox("Compare Two Finals Years")
compare_nationality = st.sidebar.checkbox("Compare by Nationality")

# Automatic adjustment based on selection
if compare_finals:
    collection_type = "finals"
else:
    collection_type = st.sidebar.selectbox("Type", ["grades", "finals"])

year_options = {
    "grades": ["2019", "2020", "2021", "2022", "2024"],
    "finals": ["2019", "2020", "2021", "2022", "2023"]
}

# Only show Year select if not comparing finals
if not compare_finals:
    collection_year = st.sidebar.selectbox("Year", year_options[collection_type])
    collection_name = f"{collection_type}_{collection_year}"
    collection = db[collection_name]

# Finals years dropdowns for comparison
finals_year_1, finals_year_2 = None, None
if compare_finals:
    finals_year_1 = st.sidebar.selectbox("Finals Year 1", year_options["finals"], index=4, key="year1")
    finals_year_2 = st.sidebar.selectbox("Finals Year 2", year_options["finals"], index=3, key="year2")

# Sidebar - Search
search_text = st.sidebar.text_input("Search by School or Code")

# Helper function to clean ObjectIds
def clean_data(data):
    for doc in data:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    return data

# Helper pipeline for Top 10 Schools
def top_schools_pipeline():
    return [
        {"$addFields": {
            "totalScore": {"$avg": [
                "$romanian_grade_final",
                "$mandatory_grade_final",
                "$chosen_grade_final"
            ]}
        }},
        {"$group": {
            "_id": "$full_school_name",
            "avgScore": {"$avg": "$totalScore"},
            "studentCount": {"$sum": 1}
        }},
        {"$sort": {"avgScore": -1}},
        {"$limit": 10}
    ]

# ---- Comparison Mode: Finals Year vs Year ----
if compare_finals and finals_year_1 and finals_year_2:
    st.subheader(f"📊 Top 10 Schools: Finals {finals_year_1} vs {finals_year_2}")

    df1 = pd.DataFrame(clean_data(list(db[f"finals_{finals_year_1}"].aggregate(top_schools_pipeline())))).rename(columns={"avgScore": f"avgScore_{finals_year_1}"})
    df2 = pd.DataFrame(clean_data(list(db[f"finals_{finals_year_2}"].aggregate(top_schools_pipeline())))).rename(columns={"avgScore": f"avgScore_{finals_year_2}"})

    merged = pd.merge(df1, df2, on="_id", how="inner").sort_values(by=f"avgScore_{finals_year_1}", ascending=False)
    st.dataframe(merged)

    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(merged))
    ax.bar([i - 0.2 for i in x], merged[f"avgScore_{finals_year_1}"], width=0.4, label=finals_year_1, align="center")
    ax.bar([i + 0.2 for i in x], merged[f"avgScore_{finals_year_2}"], width=0.4, label=finals_year_2, align="center")
    ax.set_xticks(x)
    ax.set_xticklabels(merged["_id"], rotation=45, ha="right")
    ax.set_ylabel("Average Score")
    ax.set_title(f"Top 10 Schools: Finals {finals_year_1} vs {finals_year_2}")
    ax.legend()
    st.pyplot(fig)

# ---- Comparison by Nationality ----
elif compare_nationality:
    st.subheader("🌍 Average Score by Nationality")

    if collection_type == "grades":
        pipeline = [
            {"$group": {
                "_id": "$nationality",
                "avgScore": {"$avg": "$avg"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"avgScore": -1}}
        ]
    else:
        pipeline = [
            {"$addFields": {
                "totalScore": {"$avg": [
                    "$romanian_grade_final",
                    "$mandatory_grade_final",
                    "$chosen_grade_final"]}},
            },
            {"$group": {
                "_id": "$nationality",
                "avgScore": {"$avg": "$totalScore"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"avgScore": -1}}
        ]

    data = clean_data(list(collection.aggregate(pipeline)))
    df = pd.DataFrame(data)
    st.dataframe(df)
    if not df.empty:
        st.bar_chart(df.set_index("_id")["avgScore"])

# ---- Standard View with Search ----
else:
    st.subheader(f"📃 Data from `{collection_name}`")

    query = {}
    if search_text:
        if collection_type == "grades":
            query = {"$or": [
                {"schoolName": {"$regex": search_text, "$options": "i"}},
                {"shortSchoolName": {"$regex": search_text, "$options": "i"}}
            ]}
        else:
            query = {"$or": [
                {"school": {"$regex": search_text, "$options": "i"}},
                {"code": {"$regex": search_text, "$options": "i"}}
            ]}

    data = clean_data(list(collection.find(query)))
    df = pd.DataFrame(data)

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No matching data found.")