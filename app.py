import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# Load Data
# ---------------------------
df = pd.read_csv("student_data.csv")

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("Dashboard Filters")

min_marks = int(df["Marks"].min())
max_marks = int(df["Marks"].max())

selected_marks = st.sidebar.slider(
    "Filter by Marks",
    min_marks,
    max_marks,
    (min_marks, max_marks)
)

filtered_df = df[
    (df["Marks"] >= selected_marks[0]) &
    (df["Marks"] <= selected_marks[1])
]

search = st.sidebar.text_input("Search Student")

if search:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search, case=False)
    ]

st.sidebar.download_button(
    "Download CSV",
    filtered_df.to_csv(index=False),
    "students.csv",
    "text/csv"
)

# ---------------------------
# Title
# ---------------------------
st.title("📊 Student Performance Dashboard")
st.markdown("---")

# ---------------------------
# KPI Cards
# ---------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("👨‍🎓 Total Students", len(filtered_df))
c2.metric("📈 Average Marks", round(filtered_df["Marks"].mean(), 2))
c3.metric("🏆 Highest Marks", filtered_df["Marks"].max())
c4.metric("📉 Lowest Marks", filtered_df["Marks"].min())

st.markdown("---")

# ---------------------------
# Charts
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Bar Chart")

    fig = px.bar(
        filtered_df,
        x="Name",
        y="Marks",
        color="Marks",
        text="Marks"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Line Chart")

    fig = px.line(
        filtered_df,
        x="Name",
        y="Marks",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Pie Chart
# ---------------------------
st.subheader("🥧 Marks Distribution")

fig = px.pie(
    filtered_df,
    names="Name",
    values="Marks"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Top Performer
# ---------------------------
st.subheader("⭐ Top Performer")

top = filtered_df.loc[filtered_df["Marks"].idxmax()]

st.success(
    f"{top['Name']} scored the highest marks: {top['Marks']}"
)

# ---------------------------
# Table
# ---------------------------
st.subheader("📋 Student Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)
