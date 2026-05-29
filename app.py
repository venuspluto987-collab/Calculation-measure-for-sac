# =====================================================
# SAC ANALYTICS CLOUD - FINAL CLEAN UI VERSION
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
# UPLOAD
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
# CHECK
# =====================================================

if df is None:
    st.info("Upload file to start")
    st.stop()

if df.empty:
    st.warning("Empty dataset")
    st.stop()

# =====================================================
# DETECT MODEL
# =====================================================

measures = []
dimensions = []

for c in df.columns:
    if pd.api.types.is_numeric_dtype(df[c]) and "id" not in c.lower():
        measures.append(c)
    else:
        dimensions.append(c)

# =====================================================
# MODEL PAGE (FIXED UI)
# =====================================================

if menu == "Model":

    st.subheader("📐 Data Model")

    c1, c2 = st.columns(2)

    # ================= DIMENSIONS =================
    with c1:
        st.markdown("### 📁 Dimensions")

        if len(dimensions) == 0:
            st.info("No Dimensions Found")

        for d in dimensions:
            st.markdown(
                f"""
                <div style="
                    padding:6px;
                    margin:4px 0;
                    border-radius:6px;
                    background:#f0f2f6;
                    font-size:14px;
                ">
                    📌 {d}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ================= MEASURES =================
    with c2:
        st.markdown("### 📊 Measures")

        if len(measures) == 0:
            st.info("No Measures Found")

        for m in measures:
            st.markdown(
                f"""
                <div style="
                    padding:6px;
                    margin:4px 0;
                    border-radius:6px;
                    background:#e8f4ff;
                    font-size:14px;
                ">
                    📈 {m}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()
    st.subheader("📄 Data Preview")
    st.dataframe(df, use_container_width=True)

# =====================================================
# STORY BUILDER
# =====================================================

elif menu == "Story":

    st.subheader("📊 SAC Story Builder")

    calc_cols = [c for c in df.columns if c not in measures + dimensions]

    left, right = st.columns(2)

    with left:

        st.markdown("### 📁 Data Explorer")

        view = st.selectbox(
            "View",
            ["Main Table", "Calculated Fields", "Planning", "Forecast"]
        )

        if view == "Main Table":
            st.dataframe(df, use_container_width=True)

        elif view == "Calculated Fields":
            st.dataframe(df[calc_cols + measures], use_container_width=True)

        elif view == "Planning":
            plan_cols = [c for c in df.columns if any(x in c.lower() for x in ["alloc","version","copy"])]
            st.dataframe(df[plan_cols + measures], use_container_width=True)

        elif view == "Forecast":
            fc = [c for c in df.columns if "forecast" in c.lower()]
            st.dataframe(df[fc + measures], use_container_width=True)

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

    # ================= VERSION =================
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
                new[m] = new[m] * 1.1

                df = pd.concat([df, new], ignore_index=True)
                st.session_state.df = df

                st.success("Converted")
                st.dataframe(df)

    # ================= COPY =================
    elif func == "Copy":

        m = st.selectbox("Measure", measures)
        c = st.text_input("New Column", "Copy")

        if st.button("Run"):
            df[c] = df[m] * 1.1
            st.session_state.df = df
            st.dataframe(df)

    # ================= ALLOCATION =================
    elif func == "Allocation":

        m = st.selectbox("Driver", measures)
        amt = st.number_input("Amount", 100000.0)
        c = st.text_input("Column", "Alloc")

        if st.button("Run"):
            df[c] = (df[m] / df[m].sum()) * amt
            st.session_state.df = df
            st.dataframe(df)

    # ================= CROSS MODEL =================
    elif func == "Cross Model":

        f = st.file_uploader("Upload", type=["csv","xlsx"])

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
    elif func == "Data Action":

        m = st.selectbox("Measure", measures)
        v = st.number_input("Value", 10.0)

        if st.button("Run"):
            df[m] = df[m] + v
            st.session_state.df = df
            st.dataframe(df)

    # ================= FACT DELETE =================
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
    fdf["Forecast"] = fdf[m] * (1 + p / 100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=fdf[m], name="Actual"))
    fig.add_trace(go.Scatter(y=fdf["Forecast"], name="Forecast"))

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fdf)

else:

    st.info("Upload file")
