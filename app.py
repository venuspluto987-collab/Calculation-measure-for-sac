# =====================================================
# SAC STYLE ANALYTICS + PLANNING APP
# FULL ENTERPRISE VERSION
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

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        SAC Analytics
    </div>
    """,
    unsafe_allow_html=True
)

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

st.markdown(
    """
    <div class="main-title">
        SAC Planning & Analytics
    </div>
    """,
    unsafe_allow_html=True
)

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
# DATAFRAME
# =====================================================

df = st.session_state.df

# =====================================================
# MAIN
# =====================================================

if df is not None:

    # =====================================================
    # EMPTY DATA CHECK
    # =====================================================

    if df.empty:

        st.warning("Uploaded file is empty")
        st.stop()

    # =====================================================
    # DETECT MEASURES / DIMENSIONS
    # =====================================================

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

    # =====================================================
    # MODEL PAGE
    # =====================================================

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
            use_container_width=True,
            height=400
        )

        st.divider()

        # =====================================================
        # SAC CALCULATIONS
        # =====================================================

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

    # =====================================================
    # STORY PAGE
    # =====================================================

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

    # =====================================================
    # PLANNING PAGE
    # =====================================================

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

        # =====================================================
        # VERSION MANAGEMENT
        # =====================================================

        if planning_type == "Version Management":

            version_type = st.selectbox(
                "Version Type",
                [
                    "Actual",
                    "Budget",
                    "Forecast",
                    "Planning"
                ]
            )

            version_column = st.text_input(
                "Version Column",
                "Version"
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

        # =====================================================
        # COPY MODEL
        # =====================================================

        elif planning_type == "Copy Model":

            source_measure = st.selectbox(
                "Source Measure",
                measures
            )

            target_measure = st.text_input(
                "Target Measure",
                "Copied_Value"
            )

            increase_percent = st.number_input(
                "Increase %",
                value=0.0
            )

            if st.button("Run Copy"):

                df[target_measure] = (
                    df[source_measure]
                    * (
                        1
                        + increase_percent / 100
                    )
                ).round(2)

                st.session_state.df = df

                st.success("Copy Completed")

                st.dataframe(
                    df,
                    use_container_width=True
                )

        # =====================================================
        # ALLOCATION
        # =====================================================

        elif planning_type == "Allocation":

            allocation_measure = st.selectbox(
                "Driver Measure",
                measures
            )

            allocation_amount = st.number_input(
                "Allocation Amount",
                value=100000.0
            )

            target_column = st.text_input(
                "Allocated Column",
                "Allocated_Value"
            )

            if st.button("Run Allocation"):

                total = (
                    df[allocation_measure]
                    .sum()
                )

                df[target_column] = (
                    (
                        df[allocation_measure]
                        / total
                    )
                    * allocation_amount
                ).round(2)

                st.session_state.df = df

                st.success(
                    "Allocation Completed"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

        # =====================================================
        # CROSS MODEL
        # =====================================================

        elif planning_type == "Cross Model":

            uploaded_cross = st.file_uploader(
                "Upload Cross Model",
                type=["csv", "xlsx"],
                key="cross_model"
            )

            if uploaded_cross is not None:

                try:

                    if uploaded_cross.name.endswith(".csv"):

                        cross_df = pd.read_csv(
                            uploaded_cross
                        )

                    else:

                        cross_df = pd.read_excel(
                            uploaded_cross
                        )

                    st.dataframe(
                        cross_df,
                        use_container_width=True
                    )

                    common_columns = list(
                        set(df.columns)
                        &
                        set(cross_df.columns)
                    )

                    if len(common_columns) > 0:

                        join_column = st.selectbox(
                            "Join Column",
                            common_columns
                        )

                        join_type = st.selectbox(
                            "Join Type",
                            [
                                "left",
                                "right",
                                "inner",
                                "outer"
                            ]
                        )

                        if st.button(
                            "Run Cross Model"
                        ):

                            merged_df = pd.merge(
                                df,
                                cross_df,
                                on=join_column,
                                how=join_type
                            )

                            st.session_state.df = merged_df

                            st.success(
                                "Cross Model Completed"
                            )

                            st.dataframe(
                                merged_df,
                                use_container_width=True
                            )

                    else:

                        st.warning(
                            "No common columns found"
                        )

                except Exception as e:

                    st.error(
                        f"Cross Model Error: {e}"
                    )

        # =====================================================
        # FORECAST PLANNING
        # =====================================================

        elif planning_type == "Forecast Planning":

            forecast_measure = st.selectbox(
                "Forecast Measure",
                measures
            )

            forecast_percent = st.slider(
                "Forecast Increase %",
                1,
                100,
                10
            )

            forecast_column = st.text_input(
                "Forecast Column",
                "Forecast_Value"
            )

            if st.button("Run Forecast Planning"):

                df[forecast_column] = (
                    df[forecast_measure]
                    * (
                        1
                        + forecast_percent / 100
                    )
                ).round(2)

                st.session_state.df = df

                st.success(
                    "Forecast Planning Completed"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

        # =====================================================
        # DATA ACTION
        # =====================================================

        elif planning_type == "Data Action":

            data_action = st.selectbox(
                "Data Action Type",
                [
                    "Increase Values",
                    "Decrease Values",
                    "Multiply Values",
                    "Replace Null",
                    "Convert Negative to Positive"
                ]
            )

            action_measure = st.selectbox(
                "Measure",
                measures
            )

            action_value = st.number_input(
                "Action Value",
                value=10.0
            )

            if st.button("Run Data Action"):

                try:

                    if data_action == "Increase Values":

                        df[action_measure] = (
                            df[action_measure]
                            + action_value
                        )

                    elif data_action == "Decrease Values":

                        df[action_measure] = (
                            df[action_measure]
                            - action_value
                        )

                    elif data_action == "Multiply Values":

                        df[action_measure] = (
                            df[action_measure]
                            * action_value
                        )

                    elif data_action == "Replace Null":

                        df[action_measure] = (
                            df[action_measure]
                            .fillna(action_value)
                        )

                    elif data_action == "Convert Negative to Positive":

                        df[action_measure] = np.abs(
                            df[action_measure]
                        )

                    st.session_state.df = df

                    st.success(
                        "Data Action Completed"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Data Action Error: {e}"
                    )

        # =====================================================
        # FACT DELETION
        # =====================================================

        elif planning_type == "Fact Deletion":

            delete_measure = st.selectbox(
                "Measure",
                measures
            )

            condition = st.selectbox(
                "Condition",
                [
                    "<",
                    ">",
                    "=",
                    "<=",
                    ">="
                ]
            )

            threshold = st.number_input(
                "Threshold Value",
                value=1000.0
            )

            if st.button("Run Fact Deletion"):

                try:

                    original_rows = len(df)

                    if condition == "<":

                        updated_df = df[
                            df[delete_measure]
                            >= threshold
                        ]

                    elif condition == ">":

                        updated_df = df[
                            df[delete_measure]
                            <= threshold
                        ]

                    elif condition == "=":

                        updated_df = df[
                            df[delete_measure]
                            != threshold
                        ]

                    elif condition == "<=":

                        updated_df = df[
                            df[delete_measure]
                            > threshold
                        ]

                    elif condition == ">=":

                        updated_df = df[
                            df[delete_measure]
                            < threshold
                        ]

                    df = updated_df.copy()

                    st.session_state.df = df

                    deleted_rows = (
                        original_rows
                        - len(df)
                    )

                    st.success(
                        f"{deleted_rows} rows deleted successfully"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Fact Deletion Error: {e}"
                    )

    # =====================================================
    # FORECAST PAGE
    # =====================================================

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
