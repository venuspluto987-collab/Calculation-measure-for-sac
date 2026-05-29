# =====================================================
# SAC ANALYTICS + PLANNING + STORY BUILDER (FINAL)
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

st.sidebar.title("SAC Analytics")

menu = st.sidebar.radio(
    "Navigation",
    ["Model", "Story", "Planning", "Forecast"]
)

# =====================================================
# TITLE
# =====================================================

st.title("📊 SAC Planning & Analytics Platform")

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith("csv"):
        st.session_state.df = pd.read_csv(uploaded_file)
    else:
        st.session_state.df = pd.read_excel(uploaded_file)

df = st.session_state.df

# =====================================================
# CHECK DATA
# =====================================================

if df is None:
    st.info("Upload a file to start")
    st.stop()

if df.empty:
    st.warning("Empty dataset")
    st.stop()

# =====================================================
# DETECT MEASURES / DIMENSIONS
# =====================================================

measures = []
dimensions = []

for c in df.columns:
    if pd.api.types.is_numeric_dtype(df[c]) and "id" not in c.lower():
        measures.append(c)
    else:
        dimensions.append(c)

# =====================================================
# MODEL PAGE
# =====================================================

if menu == "Model":

    st.subheader("📐 Data Model")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Dimensions")
        st.write(dimensions)

    with c2:
        st.markdown("### Measures")
        st.write(measures)

    st.divider()
    st.dataframe(df, use_container_width=True)

    # =================================================
    # CALCULATIONS ENGINE
    # =================================================

    st.subheader("🧮 SAC Calculations")

    calc_type = st.selectbox(
        "Calculation Type",
        [
            "Addition","Subtraction","Multiplication","Division",
            "Percentage","Growth %","Running Total","Moving Average",
            "Rank","Variance","Variance %","Median","Std Dev",
            "Min","Max","Count","Log","Sqrt",
            "IF Condition","Custom Formula"
        ]
    )

    calc_name = st.text_input("Calculated Column Name", "Calc")

    m1 = st.selectbox("Measure 1", measures, key="m1")
    m2 = st.selectbox("Measure 2", measures, key="m2")

    formula = ""
    if calc_type == "Custom Formula":
        formula = st.text_input("Formula (use column names)")

    if calc_type == "IF Condition":
        op = st.selectbox("Condition", [">","<","=",">=","<="])
        thr = st.number_input("Threshold", value=0.0)
        t = st.number_input("True Value", value=1.0)
        f = st.number_input("False Value", value=0.0)

    if st.button("Run Calculation"):

        if calc_type == "Addition":
            df[calc_name] = df[m1] + df[m2]

        elif calc_type == "Subtraction":
            df[calc_name] = df[m1] - df[m2]

        elif calc_type == "Multiplication":
            df[calc_name] = df[m1] * df[m2]

        elif calc_type == "Division":
            df[calc_name] = np.where(df[m2]!=0, df[m1]/df[m2], 0)

        elif calc_type == "Percentage":
            df[calc_name] = (df[m1]/df[m1].sum())*100

        elif calc_type == "Growth %":
            df[calc_name] = df[m1].pct_change()*100

        elif calc_type == "Running Total":
            df[calc_name] = df[m1].cumsum()

        elif calc_type == "Moving Average":
            df[calc_name] = df[m1].rolling(3).mean()

        elif calc_type == "Rank":
            df[calc_name] = df[m1].rank(ascending=False)

        elif calc_type == "Variance":
            df[calc_name] = df[m1] - df[m2]

        elif calc_type == "Variance %":
            df[calc_name] = np.where(df[m2]!=0, ((df[m1]-df[m2])/df[m2])*100, 0)

        elif calc_type == "Median":
            df[calc_name] = df[m1].median()

        elif calc_type == "Std Dev":
            df[calc_name] = df[m1].std()

        elif calc_type == "Min":
            df[calc_name] = df[m1].min()

        elif calc_type == "Max":
            df[calc_name] = df[m1].max()

        elif calc_type == "Count":
            df[calc_name] = df[m1].count()

        elif calc_type == "Log":
            df[calc_name] = np.log1p(df[m1])

        elif calc_type == "Sqrt":
            df[calc_name] = np.sqrt(df[m1])

        elif calc_type == "IF Condition":
            if op == ">":
                df[calc_name] = np.where(df[m1]>thr, t, f)
            elif op == "<":
                df[calc_name] = np.where(df[m1]<thr, t, f)
            elif op == "=":
                df[calc_name] = np.where(df[m1]==thr, t, f)
            elif op == ">=":
                df[calc_name] = np.where(df[m1]>=thr, t, f)
            elif op == "<=":
                df[calc_name] = np.where(df[m1]<=thr, t, f)

        elif calc_type == "Custom Formula":
            df[calc_name] = df.eval(formula)

        df[calc_name] = pd.to_numeric(df[calc_name], errors="coerce").round(2)

        st.session_state.df = df
        st.success("Calculation created")
        st.dataframe(df, use_container_width=True)

# =====================================================
# STORY BUILDER (FULL)
# =====================================================

elif menu == "Story":

    st.subheader("📊 SAC Story Builder")

    calc_cols = [c for c in df.columns if c not in measures + dimensions]

    left, right = st.columns(2)

    # ================= LEFT =================

    with left:

        st.markdown("### 📁 Data Explorer")

        view = st.selectbox(
            "View",
            ["Main Table","Calculated","Planning","Forecast"]
        )

        if view == "Main Table":
            st.dataframe(df, use_container_width=True)

        elif view == "Calculated":
            st.dataframe(df[calc_cols + measures], use_container_width=True)

        elif view == "Planning":
            plan_cols = [c for c in df.columns if any(x in c.lower() for x in ["alloc","version","copy"])]
            st.dataframe(df[plan_cols + measures], use_container_width=True)

        elif view == "Forecast":
            fc = [c for c in df.columns if "forecast" in c.lower()]
            st.dataframe(df[fc + measures], use_container_width=True)

    # ================= RIGHT =================

    with right:

        st.markdown("### 📈 Charts")

        x = st.selectbox("X Axis", dimensions)
        y = st.selectbox("Y Axis", measures)

        chart = st.selectbox(
            "Chart Type",
            ["Bar","Line","Pie","Scatter","Trend"]
        )

        if chart == "Bar":
            fig = px.bar(df, x=x, y=y)

        elif chart == "Line":
            fig = px.line(df, x=x, y=y)

        elif chart == "Pie":
            fig = px.pie(df, names=x, values=y)

        elif chart == "Scatter":
            fig = px.scatter(df, x=x, y=y)

        elif chart == "Trend":
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=df[y], name="Actual"))
            fig.add_trace(go.Scatter(y=df[y]*1.1, name="Forecast"))

        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.dataframe(df, use_container_width=True)

# =====================================================
# PLANNING
# =====================================================

elif menu == "Planning":

    st.subheader("📌 Planning")

    func = st.selectbox(
        "Function",
        ["Version","Copy","Allocation","Cross Model","Data Action","Fact Delete"]
    )

    # VERSION FIXED
    if func == "Version":

        col = st.text_input("Version Column", "Version")

        if col not in df.columns:
            df[col] = "Actual"

        action = st.selectbox("Action", ["Create","Convert"])

        if action == "Create":

            v = st.selectbox("Version", ["Actual","Budget","Forecast","Planning"])

            if st.button("Create"):
                df[col] = v
                st.session_state.df = df
                st.success("Created")
                st.dataframe(df)

        else:

            s = st.selectbox("Source", df[col].unique())
            t = st.selectbox("Target", ["Actual","Budget","Forecast","Planning"])

            m = st.selectbox("Measure", measures)

            if st.button("Convert"):

                mask = df[col] == s
                new = df[mask].copy()

                new[col] = t
                new[m] = new[m]*1.1

                df = pd.concat([df,new], ignore_index=True)

                st.session_state.df = df
                st.success("Converted")
                st.dataframe(df)

    elif func == "Copy":

        m = st.selectbox("Measure", measures)
        c = st.text_input("New Column", "Copy")

        if st.button("Run"):
            df[c] = df[m]*1.1
            st.session_state.df = df
            st.dataframe(df)

    elif func == "Allocation":

        m = st.selectbox("Driver", measures)
        amt = st.number_input("Amount", 100000.0)
        c = st.text_input("Column", "Alloc")

        if st.button("Run"):
            df[c] = (df[m]/df[m].sum())*amt
            st.session_state.df = df
            st.dataframe(df)

    elif func == "Cross Model":

        f = st.file_uploader("Upload", type=["csv","xlsx"])

        if f:

            df2 = pd.read_csv(f) if f.name.endswith("csv") else pd.read_excel(f)

            common = list(set(df.columns)&set(df2.columns))

            if common:

                j = st.selectbox("Join", common)

                if st.button("Merge"):

                    df = pd.merge(df, df2, on=j)
                    st.session_state.df = df
                    st.dataframe(df)

    elif func == "Data Action":

        m = st.selectbox("Measure", measures)
        v = st.number_input("Value", 10.0)

        if st.button("Run"):
            df[m] = df[m] + v
            st.session_state.df = df
            st.dataframe(df)

    elif func == "Fact Delete":

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
    fdf["Forecast"] = fdf[m]*(1+p/100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=fdf[m], name="Actual"))
    fig.add_trace(go.Scatter(y=fdf["Forecast"], name="Forecast"))

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fdf)

else:

    st.info("Upload file")
