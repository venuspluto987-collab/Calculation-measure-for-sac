# =====================================================
# SAC ANALYTICS CLOUD - FULL CALCULATION UPGRADE
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SAC Analytics", layout="wide")

if "df" not in st.session_state:
    st.session_state.df = None

df = st.session_state.df

# =====================================================
# UPLOAD
# =====================================================

file = st.file_uploader("Upload File", type=["csv","xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
    st.session_state.df = df

df = st.session_state.df

if df is None:
    st.info("Upload file")
    st.stop()

# =====================================================
# DETECT MODEL
# =====================================================

measures = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
dimensions = [c for c in df.columns if c not in measures]

# =====================================================
# NAV
# =====================================================

menu = st.sidebar.radio("Menu", ["Model","Story","Planning","Forecast"])

# =====================================================
# MODEL PAGE (FULL CALC ENGINE)
# =====================================================

if menu == "Model":

    st.title("📐 Model View")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dimensions")
        for d in dimensions:
            st.write("📌", d)

    with col2:
        st.subheader("Measures")
        for m in measures:
            st.write("📊", m)

    st.divider()
    st.dataframe(df, use_container_width=True)

    # =====================================================
    # CALC ENGINE (FULL SAC STYLE)
    # =====================================================

    st.subheader("🧮 SAC Calculation Engine")

    calc_type = st.selectbox(
        "Calculation Type",
        [
            # Arithmetic
            "Add","Subtract","Multiply","Divide",

            # Aggregations
            "Sum","Average","Min","Max","Count","Median",

            # Time / Trend
            "Running Total","Moving Average","Growth %","Rank",

            # Financial
            "Variance","Variance %","Percent of Total",

            # Math
            "Log","Square Root","Absolute","Power",

            # Conditional
            "IF Condition",

            # Advanced
            "Z-Score",
            "Custom Formula"
        ]
    )

    calc_name = st.text_input("Calculated Field Name", "New_Calc")

    m1 = st.selectbox("Measure 1", measures, key="m1")
    m2 = st.selectbox("Measure 2", measures, key="m2")

    formula = ""
    if calc_type == "Custom Formula":
        formula = st.text_input("Formula (use column names)")

    # IF CONDITION
    if calc_type == "IF Condition":
        op = st.selectbox("Operator", [">","<","=",">=","<="])
        thr = st.number_input("Threshold", value=0.0)
        tval = st.number_input("True Value", value=1.0)
        fval = st.number_input("False Value", value=0.0)

    if st.button("Run Calculation"):

        try:

            # =========================
            # ARITHMETIC
            # =========================
            if calc_type == "Add":
                df[calc_name] = df[m1] + df[m2]

            elif calc_type == "Subtract":
                df[calc_name] = df[m1] - df[m2]

            elif calc_type == "Multiply":
                df[calc_name] = df[m1] * df[m2]

            elif calc_type == "Divide":
                df[calc_name] = np.where(df[m2]!=0, df[m1]/df[m2], 0)

            # =========================
            # AGGREGATIONS
            # =========================
            elif calc_type == "Sum":
                df[calc_name] = df[m1].sum()

            elif calc_type == "Average":
                df[calc_name] = df[m1].mean()

            elif calc_type == "Min":
                df[calc_name] = df[m1].min()

            elif calc_type == "Max":
                df[calc_name] = df[m1].max()

            elif calc_type == "Count":
                df[calc_name] = df[m1].count()

            elif calc_type == "Median":
                df[calc_name] = df[m1].median()

            # =========================
            # TIME / TREND
            # =========================
            elif calc_type == "Running Total":
                df[calc_name] = df[m1].cumsum()

            elif calc_type == "Moving Average":
                df[calc_name] = df[m1].rolling(3).mean()

            elif calc_type == "Growth %":
                df[calc_name] = df[m1].pct_change() * 100

            elif calc_type == "Rank":
                df[calc_name] = df[m1].rank(ascending=False)

            # =========================
            # FINANCIAL
            # =========================
            elif calc_type == "Variance":
                df[calc_name] = df[m1] - df[m2]

            elif calc_type == "Variance %":
                df[calc_name] = np.where(df[m2]!=0, ((df[m1]-df[m2])/df[m2])*100, 0)

            elif calc_type == "Percent of Total":
                df[calc_name] = (df[m1] / df[m1].sum()) * 100

            # =========================
            # MATH
            # =========================
            elif calc_type == "Log":
                df[calc_name] = np.log1p(df[m1])

            elif calc_type == "Square Root":
                df[calc_name] = np.sqrt(df[m1])

            elif calc_type == "Absolute":
                df[calc_name] = np.abs(df[m1])

            elif calc_type == "Power":
                df[calc_name] = np.power(df[m1], 2)

            # =========================
            # CONDITIONAL
            # =========================
            elif calc_type == "IF Condition":

                if op == ">":
                    df[calc_name] = np.where(df[m1] > thr, tval, fval)
                elif op == "<":
                    df[calc_name] = np.where(df[m1] < thr, tval, fval)
                elif op == "=":
                    df[calc_name] = np.where(df[m1] == thr, tval, fval)
                elif op == ">=":
                    df[calc_name] = np.where(df[m1] >= thr, tval, fval)
                elif op == "<=":
                    df[calc_name] = np.where(df[m1] <= thr, tval, fval)

            # =========================
            # ADVANCED
            # =========================
            elif calc_type == "Z-Score":
                df[calc_name] = (df[m1] - df[m1].mean()) / df[m1].std()

            elif calc_type == "Custom Formula":
                df[calc_name] = df.eval(formula)

            df[calc_name] = pd.to_numeric(df[calc_name], errors="coerce").round(2)

            st.session_state.df = df

            st.success("Calculation created successfully")
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

# =====================================================
# (Other pages unchanged from your version)
# =====================================================

elif menu == "Story":
    st.subheader("Story Page")
    st.dataframe(df)

elif menu == "Planning":
    st.subheader("Planning Page")
    st.dataframe(df)

elif menu == "Forecast":
    st.subheader("Forecast Page")
    st.dataframe(df)
