# =====================================================
# SAC ANALYTICS CLOUD - FINAL STABLE WORKING VERSION
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="SAC Analytics Cloud",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "df" not in st.session_state:
    st.session_state.df = None

df = st.session_state.df

# =====================================================
# SIDEBAR
# =====================================================

menu = st.sidebar.radio(
    "Navigation",
    ["Model", "Story", "Planning", "Forecast"]
)

st.title("📊 SAC Analytics Cloud")

# =====================================================
# UPLOAD
# =====================================================

file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)

    # SAFE CLEAN
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.fillna(0)

    st.session_state.df = df

df = st.session_state.df

if df is None:
    st.info("Upload file to start")
    st.stop()

# =====================================================
# DETECT
# =====================================================

measures = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
dimensions = [c for c in df.columns if c not in measures]

# =====================================================
# MODEL
# =====================================================

if menu == "Model":

    st.subheader("📐 Model")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Dimensions")
        for d in dimensions:
            st.write("📌", d)

    with col2:
        st.markdown("### Measures")
        for m in measures:
            st.write("📊", m)

    st.dataframe(df, use_container_width=True)

# =====================================================
# STORY
# =====================================================

elif menu == "Story":

    st.subheader("📊 Story Builder")

    x = st.selectbox("X Axis", dimensions)
    y = st.selectbox("Y Axis", measures)

    chart = st.selectbox("Chart", ["Bar","Line","Pie","Scatter"])

    if chart == "Bar":
        fig = px.bar(df, x=x, y=y)
    elif chart == "Line":
        fig = px.line(df, x=x, y=y)
    elif chart == "Pie":
        fig = px.pie(df, names=x, values=y)
    else:
        fig = px.scatter(df, x=x, y=y)

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

# =====================================================
# PLANNING
# =====================================================

elif menu == "Planning":

    st.subheader("📌 Planning Engine")

    action = st.selectbox(
        "Function",
        ["Version Copy","Allocation","Copy","Data Action","Fact Delete"]
    )

    # =====================================================
    # VERSION COPY (FIXED ACTUAL → BUDGET)
    # =====================================================

    if action == "Version Copy":

        st.markdown("### 🔁 Actual → Budget Copy")

        version_col = st.selectbox("Version Column", df.columns)
        measure = st.selectbox("Measure", measures)
        adjust = st.number_input("Adjustment %", 0.0)

        if st.button("Run Copy"):

            # CLEAN VERSION COLUMN (CRITICAL FIX)
            df[version_col] = (
                df[version_col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            actual_df = df[df[version_col] == "actual"].copy()

            if actual_df.empty:
                st.error("No 'Actual' data found in Version column")
                st.stop()

            actual_df[version_col] = "budget"
            actual_df[measure] = actual_df[measure] * (1 + adjust / 100)

            df = pd.concat([df, actual_df], ignore_index=True)

            df = df.loc[:, ~df.columns.duplicated()]

            st.session_state.df = df

            st.success("Actual successfully copied to Budget")

            st.dataframe(df, use_container_width=True)

    # =====================================================
    # ALLOCATION
    # =====================================================

    elif action == "Allocation":

        m = st.selectbox("Driver", measures)
        amt = st.number_input("Amount", 100000.0)
        c = st.text_input("Column", "Alloc")

        if st.button("Run"):

            df[c] = (df[m] / df[m].sum()) * amt
            st.session_state.df = df
            st.dataframe(df)

    # =====================================================
    # COPY
    # =====================================================

    elif action == "Copy":

        m = st.selectbox("Measure", measures)
        c = st.text_input("New Column", "Copy")

        if st.button("Run"):

            df[c] = df[m] * 1.1
            st.session_state.df = df
            st.dataframe(df)

    # =====================================================
    # DATA ACTION
    # =====================================================

    elif action == "Data Action":

        m = st.selectbox("Measure", measures)
        v = st.number_input("Add Value", 10.0)

        if st.button("Run"):

            df[m] = df[m] + v
            st.session_state.df = df
            st.dataframe(df)

    # =====================================================
    # FACT DELETE
    # =====================================================

    elif action == "Fact Delete":

        m = st.selectbox("Measure", measures)
        op = st.selectbox("Condition", ["<",">","="])
        t = st.number_input("Threshold", 100.0)

        if st.button("Run"):

            if op == "<":
                df = df[df[m] >= t]
            elif op == ">":
                df = df[df[m] <= t]
            else:
                df = df[df[m] != t]

            st.session_state.df = df
            st.dataframe(df)

# =====================================================
# FORECAST
# =====================================================

elif menu == "Forecast":

    st.subheader("📈 Forecast")

    m = st.selectbox("Measure", measures)
    p = st.slider("Growth %", 1, 100, 10)

    fdf = df.copy()
    fdf["Forecast"] = fdf[m] * (1 + p / 100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=fdf[m], name="Actual"))
    fig.add_trace(go.Scatter(y=fdf["Forecast"], name="Forecast"))

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fdf)

else:

    st.info("Upload file to start")
