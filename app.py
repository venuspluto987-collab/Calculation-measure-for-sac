# =====================================================
# SAC STYLE ANALYTICS + PLANNING APP
# FULL ENTERPRISE VERSION WITH VERSION CONVERSION
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
# LOAD CSS
# =====================================================

try:

    with open("styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

except:

    pass

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("SAC Analytics")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Model",
        "Story",
        "Planning",
        "Forecast"
    ]
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

            st.session_state.df = pd.read_csv(
                uploaded_file
            )

        else:

            st.session_state.df = pd.read_excel(
                uploaded_file
            )

    except Exception as e:

        st.error(f"File Error: {e}")
        st.stop()

# =====================================================
# MAIN DATAFRAME
# =====================================================

df = st.session_state.df

# =====================================================
# MAIN APP
# =====================================================

if df is not None:

    if df.empty:

        st.warning("Uploaded file is empty")
        st.stop()

    # =================================================
    # DETECT MEASURES / DIMENSIONS
    # =================================================

    measures = []
    dimensions = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):

            measures.append(col)

        else:

            dimensions.append(col)

    # =================================================
    # MODEL PAGE
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

        st.dataframe(
            df,
            use_container_width=True
        )

        # =============================================
        # SAC CALCULATIONS
        # =============================================

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
                "Standard Deviation",
                "Log",
                "Square Root",
                "IF Condition",
                "Custom Formula"
            ]
        )

        calc_name = st.text_input(
            "Calculated Column Name",
            "New_Calculation"
        )

        measure1 = st.selectbox(
            "Measure 1",
            measures,
            key="m1"
        )

        measure2 = st.selectbox(
            "Measure 2",
            measures,
            key="m2"
        )

        formula = ""

        if calc_type == "Custom Formula":

            formula = st.text_input(
                "Formula Example: Sales * Quantity"
            )

        if calc_type == "IF Condition":

            condition_operator = st.selectbox(
                "Condition",
                [
                    ">",
                    "<",
                    "=",
                    ">=",
                    "<="
                ]
            )

            threshold = st.number_input(
                "Threshold",
                value=100.0
            )

            true_value = st.number_input(
                "True Value",
                value=1.0
            )

            false_value = st.number_input(
                "False Value",
                value=0.0
            )

        if st.button("Run Calculation"):

            try:

                if calc_type == "Addition":

                    df[calc_name] = (
                        df[measure1]
                        + df[measure2]
                    )

                elif calc_type == "Subtraction":

                    df[calc_name] = (
                        df[measure1]
                        - df[measure2]
                    )

                elif calc_type == "Multiplication":

                    df[calc_name] = (
                        df[measure1]
                        * df[measure2]
                    )

                elif calc_type == "Division":

                    df[calc_name] = np.where(
                        df[measure2] != 0,
                        df[measure1]
                        / df[measure2],
                        0
                    )

                elif calc_type == "Percentage":

                    total = df[measure1].sum()

                    df[calc_name] = (
                        df[measure1]
                        / total
                    ) * 100

                elif calc_type == "Growth %":

                    df[calc_name] = (
                        df[measure1]
                        .pct_change()
                    ) * 100

                elif calc_type == "Running Total":

                    df[calc_name] = (
                        df[measure1]
                        .cumsum()
                    )

                elif calc_type == "Moving Average":

                    df[calc_name] = (
                        df[measure1]
                        .rolling(3)
                        .mean()
                    )

                elif calc_type == "Rank":

                    df[calc_name] = (
                        df[measure1]
                        .rank(
                            ascending=False
                        )
                    )

                elif calc_type == "Variance":

                    df[calc_name] = (
                        df[measure1]
                        - df[measure2]
                    )

                elif calc_type == "Variance %":

                    df[calc_name] = np.where(
                        df[measure2] != 0,
                        (
                            (
                                df[measure1]
                                - df[measure2]
                            )
                            / df[measure2]
                        ) * 100,
                        0
                    )

                elif calc_type == "Average":

                    df[calc_name] = (
                        df[measure1]
                        .mean()
                    )

                elif calc_type == "Min":

                    df[calc_name] = (
                        df[measure1]
                        .min()
                    )

                elif calc_type == "Max":

                    df[calc_name] = (
                        df[measure1]
                        .max()
                    )

                elif calc_type == "Count":

                    df[calc_name] = (
                        df[measure1]
                        .count()
                    )

                elif calc_type == "Median":

                    df[calc_name] = (
                        df[measure1]
                        .median()
                    )

                elif calc_type == "Standard Deviation":

                    df[calc_name] = (
                        df[measure1]
                        .std()
                    )

                elif calc_type == "Log":

                    df[calc_name] = np.log1p(
                        df[measure1]
                    )

                elif calc_type == "Square Root":

                    df[calc_name] = np.sqrt(
                        df[measure1]
                    )

                elif calc_type == "IF Condition":

                    if condition_operator == ">":

                        df[calc_name] = np.where(
                            df[measure1] > threshold,
                            true_value,
                            false_value
                        )

                    elif condition_operator == "<":

                        df[calc_name] = np.where(
                            df[measure1] < threshold,
                            true_value,
                            false_value
                        )

                    elif condition_operator == "=":

                        df[calc_name] = np.where(
                            df[measure1] == threshold,
                            true_value,
                            false_value
                        )

                    elif condition_operator == ">=":

                        df[calc_name] = np.where(
                            df[measure1] >= threshold,
                            true_value,
                            false_value
                        )

                    elif condition_operator == "<=":

                        df[calc_name] = np.where(
                            df[measure1] <= threshold,
                            true_value,
                            false_value
                        )

                elif calc_type == "Custom Formula":

                    df[calc_name] = df.eval(formula)

                df[calc_name] = (
                    df[calc_name]
                    .round(2)
                )

                st.session_state.df = df

                st.success(
                    f"{calc_name} created successfully"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"Calculation Error: {e}"
                )

    # =================================================
    # STORY PAGE
    # =================================================

    elif menu == "Story":

        st.subheader("Story Dashboard")

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.metric("Rows", len(df))

        with k2:
            st.metric("Measures", len(measures))

        with k3:
            st.metric("Dimensions", len(dimensions))

        with k4:
            st.metric("Columns", len(df.columns))

        x_axis = st.selectbox(
            "X Axis",
            dimensions
        )

        y_axis = st.selectbox(
            "Y Axis",
            measures
        )

        chart_type = st.selectbox(
            "Chart Type",
            [
                "Bar",
                "Line",
                "Pie",
                "Area",
                "Scatter",
                "Histogram",
                "Box"
            ]
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

        elif chart_type == "Histogram":

            fig = px.histogram(df, x=y_axis)

        elif chart_type == "Box":

            fig = px.box(df, x=x_axis, y=y_axis)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    # =================================================
    # PLANNING PAGE
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

        # =============================================
        # VERSION MANAGEMENT
        # =============================================

        if planning_type == "Version Management":

            version_column = st.text_input(
                "Version Column",
                "Version"
            )

            version_action = st.selectbox(
                "Version Action",
                [
                    "Create Version",
                    "Convert Version"
                ]
            )

            # =========================================
            # CREATE VERSION
            # =========================================

            if version_action == "Create Version":

                version_type = st.selectbox(
                    "Version Type",
                    [
                        "Actual",
                        "Budget",
                        "Forecast",
                        "Planning"
                    ]
                )

                if st.button("Create Version"):

                    df[version_column] = version_type

                    st.session_state.df = df

                    st.success(
                        f"{version_type} version created"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

            # =========================================
            # CONVERT VERSION
            # =========================================

            elif version_action == "Convert Version":

                if version_column not in df.columns:

                    st.warning(
                        "Version column not found"
                    )

                else:

                    available_versions = (
                        df[version_column]
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    source_version = st.selectbox(
                        "Source Version",
                        available_versions
                    )

                    target_version = st.selectbox(
                        "Target Version",
                        [
                            "Actual",
                            "Budget",
                            "Forecast",
                            "Planning"
                        ]
                    )

                    conversion_percent = st.number_input(
                        "Adjustment %",
                        value=0.0
                    )

                    selected_measure = st.selectbox(
                        "Measure",
                        measures
                    )

                    if st.button(
                        "Convert Version"
                    ):

                        try:

                            converted_df = df.copy()

                            mask = (
                                converted_df[
                                    version_column
                                ].astype(str)
                                ==
                                source_version
                            )

                            new_rows = (
                                converted_df[mask]
                                .copy()
                            )

                            new_rows[
                                version_column
                            ] = target_version

                            new_rows[
                                selected_measure
                            ] = (
                                new_rows[
                                    selected_measure
                                ]
                                * (
                                    1
                                    + conversion_percent
                                    / 100
                                )
                            ).round(2)

                            converted_df = pd.concat(
                                [
                                    converted_df,
                                    new_rows
                                ],
                                ignore_index=True
                            )

                            st.session_state.df = (
                                converted_df
                            )

                            st.success(
                                f"{source_version} converted to {target_version}"
                            )

                            st.dataframe(
                                converted_df,
                                use_container_width=True
                            )

                        except Exception as e:

                            st.error(
                                f"Version Conversion Error: {e}"
                            )

    # =================================================
    # FORECAST PAGE
    # =================================================

    elif menu == "Forecast":

        st.subheader("Forecast Analysis")

        forecast_measure = st.selectbox(
            "Measure",
            measures
        )

        forecast_percent = st.slider(
            "Forecast Increase %",
            1,
            100,
            10
        )

        forecast_df = df.copy()

        forecast_df["Forecast"] = (
            forecast_df[forecast_measure]
            * (
                1
                + forecast_percent / 100
            )
        ).round(2)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=forecast_df[forecast_measure],
                mode="lines",
                name="Actual"
            )
        )

        fig.add_trace(
            go.Scatter(
                y=forecast_df["Forecast"],
                mode="lines",
                name="Forecast"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            forecast_df,
            use_container_width=True
        )

else:

    st.info(
        "Upload CSV or Excel File"
    )
