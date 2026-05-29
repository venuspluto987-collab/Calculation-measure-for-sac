# =====================================================
# SAC STYLE ANALYTICS + PLANNING APP (FINAL STABLE VERSION)
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
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
# CSS
# =====================================================

try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

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

st.title("📊 SAC Planning & Analytics")

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"File Error: {e}")
        st.stop()

df = st.session_state.df

# =====================================================
# MAIN CHECK
# =====================================================

if df is not None:

    if df.empty:
        st.warning("Uploaded file is empty")
        st.stop()

    # =================================================
    # AUTO DETECT
    # =================================================

    measures = []
    dimensions = []

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) and "id" not in col.lower():
            measures.append(col)
        else:
            dimensions.append(col)

    # =================================================
    # MODEL
    # =================================================

    if menu == "Model":

        st.subheader("Model Structure")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### Dimensions")
            for d in dimensions:
                st.write("•", d)

        with c2:
            st.markdown("### Measures")
            for m in measures:
                st.write("•", m)

        st.divider()

        st.subheader("Preview Data")

        st.dataframe(df, use_container_width=True)

        # =================================================
        # SAC CALCULATIONS (ENHANCED)
        # =================================================

        st.subheader("SAC Calculations")

        calc_type = st.selectbox(
            "Calculation Type",
            [
                "Addition",
                "Subtraction",
                "Multiplication",
                "Division",
                "Percentage",
                "Growth %",
                "Running Total",
                "Moving Average",
                "Rank",
                "Variance",
                "Variance %",
                "Average",
                "Min",
                "Max",
                "Count",
                "Median",
                "Std Dev",
                "Log",
                "Sqrt",
                "IF Condition",
                "Custom Formula"
            ]
        )

        calc_name = st.text_input("Calculated Column Name", "New_Calc")

        m1 = st.selectbox("Measure 1", measures, key="m1")
        m2 = st.selectbox("Measure 2", measures, key="m2")

        formula = ""
        if calc_type == "Custom Formula":
            formula = st.text_input("Formula (use column names)")

        if calc_type == "IF Condition":
            op = st.selectbox("Condition", [">", "<", "=", ">=", "<="])
            threshold = st.number_input("Threshold", value=0.0)
            tval = st.number_input("True Value", value=1.0)
            fval = st.number_input("False Value", value=0.0)

        if st.button("Run Calculation"):

            try:

                if calc_type == "Addition":
                    df[calc_name] = df[m1] + df[m2]

                elif calc_type == "Subtraction":
                    df[calc_name] = df[m1] - df[m2]

                elif calc_type == "Multiplication":
                    df[calc_name] = df[m1] * df[m2]

                elif calc_type == "Division":
                    df[calc_name] = np.where(df[m2] != 0, df[m1] / df[m2], 0)

                elif calc_type == "Percentage":
                    df[calc_name] = (df[m1] / df[m1].sum()) * 100

                elif calc_type == "Growth %":
                    df[calc_name] = df[m1].pct_change() * 100

                elif calc_type == "Running Total":
                    df[calc_name] = df[m1].cumsum()

                elif calc_type == "Moving Average":
                    df[calc_name] = df[m1].rolling(3).mean()

                elif calc_type == "Rank":
                    df[calc_name] = df[m1].rank(ascending=False)

                elif calc_type == "Variance":
                    df[calc_name] = df[m1] - df[m2]

                elif calc_type == "Variance %":
                    df[calc_name] = np.where(df[m2] != 0, ((df[m1] - df[m2]) / df[m2]) * 100, 0)

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

                elif calc_type == "Std Dev":
                    df[calc_name] = df[m1].std()

                elif calc_type == "Log":
                    df[calc_name] = np.log1p(df[m1])

                elif calc_type == "Sqrt":
                    df[calc_name] = np.sqrt(df[m1])

                elif calc_type == "IF Condition":

                    if op == ">":
                        df[calc_name] = np.where(df[m1] > threshold, tval, fval)
                    elif op == "<":
                        df[calc_name] = np.where(df[m1] < threshold, tval, fval)
                    elif op == "=":
                        df[calc_name] = np.where(df[m1] == threshold, tval, fval)
                    elif op == ">=":
                        df[calc_name] = np.where(df[m1] >= threshold, tval, fval)
                    elif op == "<=":
                        df[calc_name] = np.where(df[m1] <= threshold, tval, fval)

                elif calc_type == "Custom Formula":
                    df[calc_name] = df.eval(formula)

                df[calc_name] = df[calc_name].round(2)

                st.session_state.df = df

                st.success("Calculation completed")
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"Calculation Error: {e}")

    # =================================================
    # STORY
    # =================================================

    elif menu == "Story":

        st.subheader("Story Dashboard")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Rows", len(df))
        k2.metric("Measures", len(measures))
        k3.metric("Dimensions", len(dimensions))
        k4.metric("Columns", len(df.columns))

        x_axis = st.selectbox("X Axis", dimensions)
        y_axis = st.selectbox("Y Axis", measures)

        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Line", "Pie", "Area", "Scatter"]
        )

        if chart_type == "Bar":
            fig = px.bar(df, x=x_axis, y=y_axis)
        elif chart_type == "Line":
            fig = px.line(df, x=x_axis, y=y_axis)
        elif chart_type == "Pie":
            fig = px.pie(df, names=x_axis, values=y_axis)
        elif chart_type == "Area":
            fig = px.area(df, x=x_axis, y=y_axis)
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=x_axis, y=y_axis)

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)

    # =================================================
    # PLANNING
    # =================================================

    elif menu == "Planning":

        st.subheader("Planning Functions")

        planning_type = st.selectbox(
            "Planning Function",
            [
                "Version Management",
                "Copy Model",
                "Allocation",
                "Cross Model",
                "Forecast Planning",
                "Data Action",
                "Fact Deletion"
            ]
        )

        # =================================================
        # VERSION MANAGEMENT (FIXED + CONVERT)
        # =================================================

        if planning_type == "Version Management":

            version_column = st.text_input("Version Column", "Version")

            version_action = st.selectbox(
                "Version Action",
                ["Create Version", "Convert Version"]
            )

            if version_column not in df.columns:
                df[version_column] = "Actual"

            if version_action == "Create Version":

                vtype = st.selectbox(
                    "Version Type",
                    ["Actual", "Budget", "Forecast", "Planning"]
                )

                if st.button("Create Version"):
                    df[version_column] = vtype
                    st.session_state.df = df
                    st.success("Version Created")
                    st.dataframe(df)

            elif version_action == "Convert Version":

                source = st.selectbox("Source Version", df[version_column].unique())
                target = st.selectbox("Target Version", ["Actual","Budget","Forecast","Planning"])

                pct = st.number_input("Adjustment %", value=0.0)
                measure = st.selectbox("Measure", measures)

                if st.button("Convert Version"):

                    mask = df[version_column] == source
                    new_rows = df[mask].copy()

                    new_rows[version_column] = target
                    new_rows[measure] = new_rows[measure] * (1 + pct/100)

                    df = pd.concat([df, new_rows], ignore_index=True)
                    st.session_state.df = df

                    st.success("Version Converted")
                    st.dataframe(df)

        # =================================================
        # COPY MODEL
        # =================================================

        elif planning_type == "Copy Model":

            m = st.selectbox("Measure", measures)
            new_col = st.text_input("New Column", "Copy")
            pct = st.number_input("Increase %", value=0.0)

            if st.button("Run"):
                df[new_col] = df[m] * (1 + pct/100)
                st.session_state.df = df
                st.dataframe(df)

        # =================================================
        # ALLOCATION
        # =================================================

        elif planning_type == "Allocation":

            m = st.selectbox("Driver", measures)
            amt = st.number_input("Amount", value=100000.0)
            col = st.text_input("Target", "Allocated")

            if st.button("Run"):

                total = df[m].sum()
                df[col] = (df[m] / total) * amt
                st.session_state.df = df
                st.dataframe(df)

        # =================================================
        # CROSS MODEL
        # =================================================

        elif planning_type == "Cross Model":

            file2 = st.file_uploader("Upload Model", type=["csv","xlsx"])

            if file2:

                df2 = pd.read_csv(file2) if file2.name.endswith("csv") else pd.read_excel(file2)

                common = list(set(df.columns) & set(df2.columns))

                if common:

                    join = st.selectbox("Join Column", common)
                    how = st.selectbox("Join Type", ["left","right","inner","outer"])

                    if st.button("Run Cross Model"):

                        df = pd.merge(df, df2, on=join, how=how)
                        st.session_state.df = df
                        st.dataframe(df)

        # =================================================
        # FORECAST PLANNING
        # =================================================

        elif planning_type == "Forecast Planning":

            m = st.selectbox("Measure", measures)
            pct = st.slider("Forecast %", 1, 100, 10)
            col = st.text_input("Forecast Column", "Forecast")

            if st.button("Run"):
                df[col] = df[m] * (1 + pct/100)
                st.session_state.df = df
                st.dataframe(df)

        # =================================================
        # DATA ACTION
        # =================================================

        elif planning_type == "Data Action":

            action = st.selectbox(
                "Action",
                ["Increase","Decrease","Multiply","Replace Null","Abs"]
            )

            m = st.selectbox("Measure", measures)
            val = st.number_input("Value", value=10.0)

            if st.button("Run"):

                if action == "Increase":
                    df[m] = df[m] + val
                elif action == "Decrease":
                    df[m] = df[m] - val
                elif action == "Multiply":
                    df[m] = df[m] * val
                elif action == "Replace Null":
                    df[m] = df[m].fillna(val)
                elif action == "Abs":
                    df[m] = np.abs(df[m])

                st.session_state.df = df
                st.dataframe(df)

        # =================================================
        # FACT DELETION
        # =================================================

        elif planning_type == "Fact Deletion":

            m = st.selectbox("Measure", measures)
            cond = st.selectbox("Condition", ["<",">","="])
            t = st.number_input("Threshold", value=1000.0)

            if st.button("Run"):

                if cond == "<":
                    df = df[df[m] >= t]
                elif cond == ">":
                    df = df[df[m] <= t]
                elif cond == "=":
                    df = df[df[m] != t]

                st.session_state.df = df
                st.dataframe(df)

    # =================================================
    # FORECAST
    # =================================================

    elif menu == "Forecast":

        st.subheader("Forecast View")

        m = st.selectbox("Measure", measures)
        pct = st.slider("Growth %", 1, 100, 10)

        df2 = df.copy()
        df2["Forecast"] = df2[m] * (1 + pct/100)

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df2[m], name="Actual"))
        fig.add_trace(go.Scatter(y=df2["Forecast"], name="Forecast"))

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df2)

else:

    st.info("Upload CSV or Excel File")
