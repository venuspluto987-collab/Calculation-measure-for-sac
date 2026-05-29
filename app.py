# =====================================================
# SAC STYLE ANALYTICS + STORY BUILDER APP
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import uuid

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SAC Analytics Cloud",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# SESSION STATE INIT
# =====================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "stories" not in st.session_state:
    st.session_state.stories = []

# =====================================================
# SAVE TO STORY FUNCTION
# =====================================================

def save_to_story(item_type, title, payload):
    st.session_state.stories.append({
        "id": str(uuid.uuid4()),
        "type": item_type,   # chart / table / kpi
        "title": title,
        "payload": payload
    })

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("SAC Analytics")

menu = st.sidebar.radio(
    "Navigation",
    ["Model", "Story", "Planning", "Forecast", "Story Builder"]
)

# =====================================================
# TITLE
# =====================================================

st.title("SAC Planning & Analytics")

# =====================================================
# UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# =====================================================
# LOAD DATA
# =====================================================

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state.df = df

df = st.session_state.df

# =====================================================
# STOP IF NO DATA
# =====================================================

if df is None:
    st.info("Upload CSV or Excel File")
    st.stop()

# =====================================================
# DETECT TYPES
# =====================================================

measures = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
dimensions = [c for c in df.columns if c not in measures]

# =====================================================
# MODEL PAGE
# =====================================================

if menu == "Model":

    st.subheader("Model Structure")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Dimensions")
        for d in dimensions:
            st.write(d)

    with col2:
        st.markdown("### Measures")
        for m in measures:
            st.write(m)

    st.subheader("Data Preview")

    st.dataframe(df, use_container_width=True)

    # ================= SAVE TABLE =================
    if st.button("📌 Save Model Table to Story"):
        save_to_story("table", "Model Data Preview", {
            "data": df.to_dict("records")
        })
        st.success("Saved to Story Builder")

# =====================================================
# STORY PAGE
# =====================================================

elif menu == "Story":

    st.subheader("Story Dashboard")

    if not measures:
        st.warning("No measures found")
        st.stop()

    m = measures[0]

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total", round(df[m].sum(), 2))
    k2.metric("Avg", round(df[m].mean(), 2))
    k3.metric("Max", round(df[m].max(), 2))
    k4.metric("Min", round(df[m].min(), 2))

    dim = dimensions[0] if dimensions else None

    if dim:

        fig = px.bar(df, x=dim, y=m)

        st.plotly_chart(fig, use_container_width=True)

        # ================= SAVE CHART =================
        if st.button("📌 Save Chart to Story"):
            save_to_story("chart", "Story Bar Chart", {
                "x": dim,
                "y": m,
                "type": "bar"
            })
            st.success("Saved to Story Builder")

# =====================================================
# PLANNING PAGE
# =====================================================

elif menu == "Planning":

    st.subheader("Planning")

    if measures:

        m = measures[0]

        df["Planned"] = df[m] * 1.1

        st.dataframe(df)

        fig = px.line(df, y=[m, "Planned"])
        st.plotly_chart(fig)

        # ================= SAVE PLANNING =================
        if st.button("📌 Save Planning View"):
            save_to_story("chart", "Planning Forecast", {
                "x": None,
                "y": [m, "Planned"],
                "type": "line"
            })
            st.success("Saved to Story Builder")

# =====================================================
# FORECAST PAGE
# =====================================================

elif menu == "Forecast":

    st.subheader("Forecast")

    if measures:

        m = measures[0]

        df["Forecast"] = df[m] * 1.2

        fig = px.line(df, y=[m, "Forecast"])
        st.plotly_chart(fig)

        st.dataframe(df)

        # ================= SAVE FORECAST =================
        if st.button("📌 Save Forecast"):
            save_to_story("chart", "Forecast View", {
                "y": [m, "Forecast"],
                "type": "line"
            })
            st.success("Saved to Story Builder")

# =====================================================
# STORY BUILDER PAGE
# =====================================================

elif menu == "Story Builder":

    st.subheader("📌 Story Builder")

    stories = st.session_state.stories

    if not stories:
        st.info("No saved items yet")
        st.stop()

    # ================= ORDER CONTROL =================
    for i, item in enumerate(stories):

        col1, col2, col3, col4 = st.columns([4,1,1,1])

        with col1:
            st.write(f"**{item['title']}** ({item['type']})")

        with col2:
            if st.button("⬆", key=f"up_{item['id']}") and i > 0:
                stories[i], stories[i-1] = stories[i-1], stories[i]

        with col3:
            if st.button("⬇", key=f"down_{item['id']}") and i < len(stories)-1:
                stories[i], stories[i+1] = stories[i+1], stories[i]

        with col4:
            if st.button("👁 Show", key=f"show_{item['id']}"):
                st.session_state.selected_story = item

    st.divider()

    # ================= PREVIEW SELECTED =================

    selected = st.session_state.get("selected_story")

    if selected:

        st.subheader("Preview")

        if selected["type"] == "table":

            st.dataframe(pd.DataFrame(selected["payload"]["data"]))

        elif selected["type"] == "chart":

            p = selected["payload"]

            if p["type"] == "bar":
                fig = px.bar(df, x=p.get("x"), y=p["y"])

            elif p["type"] == "line":
                fig = px.line(df, y=p["y"])

            st.plotly_chart(fig, use_container_width=True)
