# =====================================================
# SAC ANALYTICS CLOUD - ADVANCED FULL APP
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

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

# =====================================================
# SAC CALC ENGINE CORE FUNCTIONS
# =====================================================

def percent_of_total(df, col):
    return (df[col] / df[col].sum()) * 100

def running_total(df, col):
    return df[col].cumsum()

def yoy_growth(df, col):
    return df[col].pct_change() * 100

def variance(actual, plan):
    return actual - plan

def variance_pct(actual, plan):
    return np.where(plan != 0, (actual - plan) / plan * 100, 0)

def index_base100(df, col):
    return (df[col] / df[col].mean()) * 100

def moving_average(df, col, window=3):
    return df[col].rolling(window).mean()

def rank_calc(df, col):
    return df[col].rank(ascending=False)

def z_score(df, col):
    return (df[col] - df[col].mean()) / df[col].std()

# =====================================================
# SAFE CUSTOM FORMULA ENGINE
# =====================================================

def safe_sac_formula(df, formula):
    expr = formula
    columns = sorted(df.columns, key=len, reverse=True)

    for col in columns:
        expr = re.sub(rf"\b{col}\b", f"df['{col}']", expr)

    return eval(expr, {"df": df, "np": np})

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

menu = st.sidebar.radio(
    "Navigation",
    ["Model", "Story", "Planning", "Forecast"]
)

st.title("📊 SAC Analytics Cloud (Advanced)")

# =====================================================
# FILE UPLOAD
# =====================================================

file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if file:
    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df = df.loc[:, ~df.columns.duplicated()]
    df = df.fillna(0)

    st.session_state.df = df

df = st.session_state.df

if df is None:
    st.info("Upload file to start")
    st.stop()

# =====================================================
# DIMENSIONS & MEASURES
# =====================================================

measures = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
dimensions = [c for c in df.columns if c not in measures]

if len(measures) == 0 or len(dimensions) == 0:
    st.warning("Need at least 1 numeric and 1 text column")
    st.stop()

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

    # =====================================================
    # SAC CALC ENGINE UI
    # =====================================================

    st.subheader("🧮 SAC Calculation Engine")

    calc_type = st.selectbox(
        "Select Calculation",
        [
            "Basic Arithmetic",
            "Percentage of Total",
            "Running Total (YTD)",
            "YoY Growth %",
            "Variance (Actual - Plan)",
            "Variance %",
            "Index (Base 100)",
            "Moving Average",
            "Ranking",
            "Z-Score",
            "Custom Formula"
        ]
    )

    new_col = st.text_input("Output Column", "SAC_Result")

    m1 = st.selectbox("Primary Measure", measures)

    op = m2 = plan = actual = None

    if calc_type == "Basic Arithmetic":
        op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
        m2 = st.selectbox("Second Measure", measures)

    elif calc_type in ["Variance (Actual - Plan)", "Variance %"]:
        actual = st.selectbox("Actual", measures)
        plan = st.selectbox("Plan", measures)

    elif calc_type == "Moving Average":
        window = st.slider("Window", 2, 20, 3)

    elif calc_type == "Custom Formula":
        formula = st.text_input("Formula", "Revenue - Cost")

    if st.button("Run SAC Calculation"):

        # =====================================================
        # BASIC ARITHMETIC
        # =====================================================
        if calc_type == "Basic Arithmetic":

            if op == "Add":
                df[new_col] = df[m1] + df[m2]
            elif op == "Subtract":
                df[new_col] = df[m1] - df[m2]
            elif op == "Multiply":
                df[new_col] = df[m1] * df[m2]
            else:
                df[new_col] = np.where(df[m2] != 0, df[m1] / df[m2], 0)

        # =====================================================
        # % TOTAL
        # =====================================================
        elif calc_type == "Percentage of Total":
            df[new_col] = percent_of_total(df, m1)

        # =====================================================
        # RUNNING TOTAL
        # =====================================================
        elif calc_type == "Running Total (YTD)":
            df[new_col] = running_total(df, m1)

        # =====================================================
        # YOY GROWTH
        # =====================================================
        elif calc_type == "YoY Growth %":
            df[new_col] = yoy_growth(df, m1)

        # =====================================================
        # VARIANCE
        # =====================================================
        elif calc_type == "Variance (Actual - Plan)":
            df[new_col] = variance(df[actual], df[plan])

        # =====================================================
        # VARIANCE %
        # =====================================================
        elif calc_type == "Variance %":
            df[new_col] = variance_pct(df[actual], df[plan])

        # =====================================================
        # INDEX
        # =====================================================
        elif calc_type == "Index (Base 100)":
            df[new_col] = index_base100(df, m1)

        # =====================================================
        # MOVING AVERAGE
        # =====================================================
        elif calc_type == "Moving Average":
            df[new_col] = moving_average(df, m1, window)

        # =====================================================
        # RANK
        # =====================================================
        elif calc_type == "Ranking":
            df[new_col] = rank_calc(df, m1)

        # =====================================================
        # Z SCORE
        # =====================================================
        elif calc_type == "Z-Score":
            df[new_col] = z_score(df, m1)

        # =====================================================
        # CUSTOM FORMULA
        # =====================================================
        elif calc_type == "Custom Formula":
            try:
                df[new_col] = safe_sac_formula(df, formula)
            except Exception as e:
                st.error(f"Formula Error: {e}")
                st.stop()

        df[new_col] = pd.to_numeric(df[new_col], errors="coerce").round(2)

        st.session_state.df = df
        st.success(f"{new_col} created successfully")
        st.dataframe(df, use_container_width=True)

# =====================================================
# STORY PAGE
# =====================================================

elif menu == "Story":

    st.subheader("📊 Story Builder")

    x = st.selectbox("X Axis", dimensions)
    y = st.selectbox("Y Axis", measures)

    chart = st.selectbox("Chart Type", ["Bar", "Line", "Pie", "Scatter"])

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
# PLANNING PAGE (MINIMAL SAFE)
# =====================================================
# =====================================================
# PLANNING PAGE (SAC-STYLE FULL ENGINE)
# =====================================================

elif menu == "Planning":

    st.subheader("📌 SAC Planning Engine")

    action = st.selectbox(
        "Planning Action",
        [
            "Copy Model",
            "Cross Model Copy",
            "Version Conversion",
            "Allocation",
            "Fact Deletion"
        ]
    )

    df = st.session_state.df

    # =====================================================
    # COPY MODEL
    # =====================================================
    if action == "Copy Model":

        st.markdown("### 📄 Copy Model (Duplicate Dataset)")

        new_name = st.text_input("New Model Name", "Model_Copy")

        if st.button("Copy Model"):

            st.session_state[new_name] = df.copy()

            st.success(f"Model '{new_name}' created successfully")
            st.dataframe(st.session_state[new_name], use_container_width=True)

    # =====================================================
    # CROSS MODEL COPY
    # =====================================================
    elif action == "Cross Model Copy":

        st.markdown("### 🔀 Cross Model Copy (Source → Target Model)")

        target_model = st.text_input("Target Model Name", "Target_Model")

        col_map = {}

        st.write("Map Columns (Source → Target)")

        for col in df.columns:
            col_map[col] = st.text_input(f"{col} →", value=col)

        if st.button("Execute Cross Model Copy"):

            new_df = df.rename(columns=col_map).copy()

            st.session_state[target_model] = new_df

            st.success(f"Cross model '{target_model}' created")
            st.dataframe(new_df, use_container_width=True)

    # =====================================================
    # VERSION CONVERSION
    # =====================================================
    elif action == "Version Conversion":

        st.markdown("### 🔄 Version Conversion (Actual → Budget / Forecast)")

        version_col = st.selectbox("Version Column (if exists)", dimensions + ["None"])

        measure = st.selectbox("Measure", measures)

        target_version = st.selectbox(
            "Target Version",
            ["Actual", "Budget", "Forecast", "Planning"]
        )

        adjust = st.number_input("Adjustment %", value=0.0)

        if st.button("Convert Version"):

            temp = df.copy()

            if version_col != "None":
                temp["Version"] = target_version
            else:
                temp["Version"] = target_version

            temp[measure] = temp[measure] * (1 + adjust / 100)

            df = pd.concat([df, temp], ignore_index=True)

            st.session_state.df = df

            st.success(f"Converted to {target_version}")
            st.dataframe(df, use_container_width=True)

    # =====================================================
    # ALLOCATION ENGINE
    # =====================================================
    elif action == "Allocation":

        st.markdown("### 📊 Driver Based Allocation")

        measure = st.selectbox("Base Measure", measures)

        total_amount = st.number_input("Total Amount to Allocate", 100000.0)

        method = st.selectbox(
            "Allocation Method",
            ["Equal Split", "Proportional (by measure)", "Custom Weight"]
        )

        new_col = st.text_input("Output Column", "Allocated_Value")

        if st.button("Run Allocation"):

            if method == "Equal Split":
                df[new_col] = total_amount / len(df)

            elif method == "Proportional (by measure)":
                df[new_col] = (df[measure] / df[measure].sum()) * total_amount

            elif method == "Custom Weight":
                weight_col = st.selectbox("Weight Column", measures)
                df[new_col] = (df[weight_col] / df[weight_col].sum()) * total_amount

            st.session_state.df = df

            st.success("Allocation completed")
            st.dataframe(df, use_container_width=True)

    # =====================================================
    # FACT DELETION
    # =====================================================
    elif action == "Fact Deletion":

        st.markdown("### 🧹 Fact Deletion Engine")

        measure = st.selectbox("Measure", measures)

        condition = st.selectbox("Condition", ["<", ">", "=", "<=", ">="])

        threshold = st.number_input("Threshold Value", 0.0)

        if st.button("Delete Facts"):

            if condition == "<":
                df = df[df[measure] >= threshold]

            elif condition == ">":
                df = df[df[measure] <= threshold]

            elif condition == "=":
                df = df[df[measure] != threshold]

            elif condition == "<=":
                df = df[df[measure] > threshold]

            elif condition == ">=":
                df = df[df[measure] < threshold]

            st.session_state.df = df

            st.success("Fact deletion completed")
            st.dataframe(df, use_container_width=True)
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
