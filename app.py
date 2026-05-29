# =====================================================
# SAC ANALYTICS CLOUD - FULL WORKING APP
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
# DETECT DIMENSIONS & MEASURES
# =====================================================

measures = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
dimensions = [c for c in df.columns if c not in measures]

# =====================================================
# MODEL PAGE
# =====================================================

if menu == "Model":

    st.subheader("📐 Model Structure")

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

    st.subheader("🧮 Calculation")

    calc = st.selectbox("Type", ["Add","Subtract","Multiply","Divide"])
    new_col = st.text_input("New Column", "Calc")

    m1 = st.selectbox("Measure 1", measures)
    m2 = st.selectbox("Measure 2", measures)

    if st.button("Run Calculation"):

        if calc == "Add":
            df[new_col] = df[m1] + df[m2]

        elif calc == "Subtract":
            df[new_col] = df[m1] - df[m2]

        elif calc == "Multiply":
            df[new_col] = df[m1] * df[m2]

        elif calc == "Divide":
            df[new_col] = np.where(df[m2] != 0, df[m1] / df[m2], 0)

        df[new_col] = pd.to_numeric(df[new_col], errors="coerce").round(2)

        st.session_state.df = df
        st.success("Calculation added")
        st.dataframe(df)

# =====================================================
# STORY PAGE
# =====================================================

elif menu == "Story":

    st.subheader("📊 Story Builder")

    x = st.selectbox("X Axis", dimensions)
    y = st.selectbox("Y Axis", measures)

    chart = st.selectbox("Chart Type", ["Bar","Line","Pie","Scatter"])

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
# PLANNING PAGE (FULL VERSION CONTROL WORKING)
# =====================================================

elif menu == "Planning":

    st.subheader("📌 Planning Engine")

    action = st.selectbox(
        "Function",
        ["Version Conversion","Allocation","Copy","Data Action","Fact Delete"]
    )

    # =====================================================
    # VERSION CONVERSION (CORE FIXED FEATURE)
    # =====================================================

    if action == "Version Conversion":

        st.markdown("### 🔁 Version Conversion (SAC Style)")

        version_col = st.selectbox("Version Column", df.columns)

        df[version_col] = (
            df[version_col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        source_version = st.selectbox(
            "Source Version",
            df[version_col].unique()
        )

        target_version = st.selectbox(
            "Target Version",
            ["actual","budget","forecast","planning"]
        )

        measure = st.selectbox("Measure", measures)

        adjust = st.number_input("Adjustment %", 0.0)

        if st.button("Convert Version"):

            temp = df[df[version_col] == source_version].copy()

            if temp.empty:
                st.error("No data found for source version")
                st.stop()

            temp[version_col] = target_version

            temp[measure] = temp[measure] * (1 + adjust / 100)

            df = pd.concat([df, temp], ignore_index=True)

            df = df.loc[:, ~df.columns.duplicated()]

            st.session_state.df = df

            st.success(f"{source_version} → {target_version} conversion done")

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
# FORECAST PAGE
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
