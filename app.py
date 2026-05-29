# =====================================================
# SAC ANALYTICS CLOUD - FULL WORKING VERSION
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

file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
    st.session_state.df = df

df = st.session_state.df

if df is None:
    st.info("Upload file")
    st.stop()

# =====================================================
# MODEL DETECTION
# =====================================================

measures = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
dimensions = [c for c in df.columns if c not in measures]

# =====================================================
# MODEL PAGE (FULL CALC ENGINE)
# =====================================================

if menu == "Model":

    st.subheader("📐 Model")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Dimensions")
        for d in dimensions:
            st.write("📌", d)

    with c2:
        st.markdown("### Measures")
        for m in measures:
            st.write("📊", m)

    st.dataframe(df, use_container_width=True)

    st.subheader("🧮 Calculation Engine")

    calc = st.selectbox(
        "Calculation Type",
        [
            "Add","Subtract","Multiply","Divide",
            "Running Total","Moving Average","Growth %",
            "Rank","Variance","Variance %",
            "Sum","Average","Min","Max",
            "IF Condition","Custom Formula"
        ]
    )

    name = st.text_input("New Column Name", "Calc")

    m1 = st.selectbox("Measure 1", measures, key="m1")
    m2 = st.selectbox("Measure 2", measures, key="m2")

    formula = ""
    if calc == "Custom Formula":
        formula = st.text_input("Formula")

    if calc == "IF Condition":
        op = st.selectbox("Operator", [">","<","=",">=","<="])
        thr = st.number_input("Threshold")
        tval = st.number_input("True")
        fval = st.number_input("False")

    if st.button("Run Calculation"):

        if calc == "Add":
            df[name] = df[m1] + df[m2]

        elif calc == "Subtract":
            df[name] = df[m1] - df[m2]

        elif calc == "Multiply":
            df[name] = df[m1] * df[m2]

        elif calc == "Divide":
            df[name] = np.where(df[m2]!=0, df[m1]/df[m2], 0)

        elif calc == "Running Total":
            df[name] = df[m1].cumsum()

        elif calc == "Moving Average":
            df[name] = df[m1].rolling(3).mean()

        elif calc == "Growth %":
            df[name] = df[m1].pct_change()*100

        elif calc == "Rank":
            df[name] = df[m1].rank(ascending=False)

        elif calc == "Variance":
            df[name] = df[m1] - df[m2]

        elif calc == "Variance %":
            df[name] = np.where(df[m2]!=0, ((df[m1]-df[m2])/df[m2])*100, 0)

        elif calc == "Sum":
            df[name] = df[m1].sum()

        elif calc == "Average":
            df[name] = df[m1].mean()

        elif calc == "Min":
            df[name] = df[m1].min()

        elif calc == "Max":
            df[name] = df[m1].max()

        elif calc == "IF Condition":
            if op == ">":
                df[name] = np.where(df[m1]>thr, tval, fval)
            elif op == "<":
                df[name] = np.where(df[m1]<thr, tval, fval)
            elif op == "=":
                df[name] = np.where(df[m1]==thr, tval, fval)
            elif op == ">=":
                df[name] = np.where(df[m1]>=thr, tval, fval)
            elif op == "<=":
                df[name] = np.where(df[m1]<=thr, tval, fval)

        elif calc == "Custom Formula":
            df[name] = df.eval(formula)

        df[name] = pd.to_numeric(df[name], errors="coerce").round(2)

        st.session_state.df = df
        st.success("Calculation Added")
        st.dataframe(df)

# =====================================================
# STORY PAGE (FIXED FULL)
# =====================================================

elif menu == "Story":

    st.subheader("📊 Story Builder")

    calc_cols = [c for c in df.columns if c not in measures + dimensions]

    left, right = st.columns(2)

    with left:

        st.markdown("### Data Explorer")

        view = st.selectbox(
            "View",
            ["Main Table","Calculated","Planning","Forecast"]
        )

        if view == "Main Table":
            st.dataframe(df, use_container_width=True)

        elif view == "Calculated":
            st.dataframe(df[calc_cols + measures], use_container_width=True)

        elif view == "Planning":
            plan_cols = [c for c in df.columns if "alloc" in c.lower() or "version" in c.lower() or "copy" in c.lower()]
            st.dataframe(df[plan_cols + measures], use_container_width=True)

        elif view == "Forecast":
            fc = [c for c in df.columns if "forecast" in c.lower()]
            st.dataframe(df[fc + measures], use_container_width=True)

    with right:

        st.markdown("### Charts")

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
# PLANNING PAGE (FULL FIXED)
# =====================================================

elif menu == "Planning":

    st.subheader("📌 Planning Engine")

    action = st.selectbox(
        "Function",
        ["Version","Copy","Allocation","Cross Model","Data Action","Fact Delete"]
    )

    # ================= VERSION =================
    if action == "Version":

        col = st.text_input("Version Column", "Version")

        if col not in df.columns:
            df[col] = "Actual"

        mode = st.selectbox("Mode", ["Create","Convert"])

        if mode == "Create":

            v = st.selectbox("Version", ["Actual","Budget","Forecast","Planning"])

            if st.button("Create Version"):
                df[col] = v
                st.session_state.df = df
                st.success("Version Created")
                st.dataframe(df)

        else:

            s = st.selectbox("Source", df[col].unique())
            t = st.selectbox("Target", ["Actual","Budget","Forecast","Planning"])

            m = st.selectbox("Measure", measures)

            if st.button("Convert"):

                temp = df[df[col] == s].copy()
                temp[col] = t
                temp[m] = temp[m] * 1.1

                df = pd.concat([df, temp], ignore_index=True)

                st.session_state.df = df
                st.success("Version Converted")
                st.dataframe(df)

    # ================= COPY =================
    elif action == "Copy":

        m = st.selectbox("Measure", measures)
        c = st.text_input("New Column", "Copy")

        if st.button("Run"):
            df[c] = df[m] * 1.1
            st.session_state.df = df
            st.dataframe(df)

    # ================= ALLOCATION =================
    elif action == "Allocation":

        m = st.selectbox("Driver", measures)
        amt = st.number_input("Amount", 100000.0)
        c = st.text_input("Column", "Alloc")

        if st.button("Run"):
            df[c] = (df[m] / df[m].sum()) * amt
            st.session_state.df = df
            st.dataframe(df)

    # ================= CROSS MODEL =================
    elif action == "Cross Model":

        f = st.file_uploader("Upload File", type=["csv","xlsx"])

        if f:

            df2 = pd.read_csv(f) if f.name.endswith("csv") else pd.read_excel(f)

            common = list(set(df.columns) & set(df2.columns))

            if common:

                j = st.selectbox("Join Column", common)

                if st.button("Merge"):
                    df = pd.merge(df, df2, on=j)
                    st.session_state.df = df
                    st.dataframe(df)

    # ================= DATA ACTION =================
    elif action == "Data Action":

        m = st.selectbox("Measure", measures)
        v = st.number_input("Add Value", 10.0)

        if st.button("Run"):
            df[m] = df[m] + v
            st.session_state.df = df
            st.dataframe(df)

    # ================= FACT DELETE =================
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
    fdf["Forecast"] = fdf[m] * (1 + p/100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=fdf[m], name="Actual"))
    fig.add_trace(go.Scatter(y=fdf["Forecast"], name="Forecast"))

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fdf)

else:

    st.info("Upload file")
