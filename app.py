# =====================================================
# SAC STYLE ANALYTICS + PLANNING APP
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SAC Analytics Cloud",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD CSS
# =====================================================

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

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
        "Calculation",
        "Planning",
        "Story",
        "Forecast"
    ],
    key="sidebar_menu"
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
    type=["csv", "xlsx"],
    key="main_upload"
)

# =====================================================
# MAIN
# =====================================================

if uploaded_file is not None:

    # =====================================================
    # READ FILE
    # =====================================================

    try:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(f"File Error: {e}")
        st.stop()

    # =====================================================
    # AUTO DETECT
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

        col1, col2 = st.columns(2)

        # ---------------- DIMENSIONS ----------------

        with col1:

            st.markdown(
                """
                <div class="card">
                    <div class="card-title">
                        Dimensions
                    </div>
                """,
                unsafe_allow_html=True
            )

            for d in dimensions:

                st.markdown(
                    f"""
                    <div class="dimension-item">
                        {d}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- MEASURES ----------------

        with col2:

            st.markdown(
                """
                <div class="card">
                    <div class="card-title">
                        Measures
                    </div>
                """,
                unsafe_allow_html=True
            )

            for m in measures:

                st.markdown(
                    f"""
                    <div class="measure-item">
                        {m}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        # =====================================================
        # DATA PREVIEW
        # =====================================================

        st.subheader("Preview Data")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

    # =====================================================
    # CALCULATION PAGE
    # =====================================================

    elif menu == "Calculation":

        st.subheader("Calculated Measures")

        calc_type = st.selectbox(
            "Calculation Type",
            [
                "Addition",
                "Subtraction",
                "Multiplication",
                "Division",
                "Profit %",
                "Growth %",
                "Running Total",
                "Rank",
                "Moving Average",
                "Variance",
                "Variance %",
                "Contribution %",
                "Average",
                "Max",
                "Min"
            ],
            key="calc_type"
        )

        # =====================================================
        # MEASURE SELECTION
        # =====================================================

        c1, c2 = st.columns(2)

        with c1:

            measure1 = st.selectbox(
                "Measure 1",
                measures,
                key="calc_measure1"
            )

        with c2:

            if calc_type in [
                "Running Total",
                "Rank",
                "Moving Average",
                "Average",
                "Max",
                "Min"
            ]:

                measure2 = None

                st.info(
                    "Second measure not required"
                )

            else:

                measure2 = st.selectbox(
                    "Measure 2",
                    measures,
                    key="calc_measure2"
                )

        # =====================================================
        # NEW COLUMN
        # =====================================================

        new_measure = st.text_input(
            "Calculated Measure Name",
            "Calculated_Measure",
            key="calc_new_measure"
        )

        # =====================================================
        # CREATE CALCULATION
        # =====================================================

        if st.button(
            "Create Calculation",
            key="create_calc_btn"
        ):

            try:

                df[measure1] = pd.to_numeric(
                    df[measure1],
                    errors="coerce"
                )

                if measure2:

                    df[measure2] = pd.to_numeric(
                        df[measure2],
                        errors="coerce"
                    )

                # =====================================================
                # CALCULATIONS
                # =====================================================

                if calc_type == "Addition":

                    df[new_measure] = (
                        df[measure1]
                        + df[measure2]
                    )

                elif calc_type == "Subtraction":

                    df[new_measure] = (
                        df[measure1]
                        - df[measure2]
                    )

                elif calc_type == "Multiplication":

                    df[new_measure] = (
                        df[measure1]
                        * df[measure2]
                    )

                elif calc_type == "Division":

                    df[new_measure] = (
                        df[measure1]
                        / df[measure2]
                    )

                elif calc_type == "Profit %":

                    df[new_measure] = (
                        (
                            df[measure1]
                            - df[measure2]
                        )
                        / df[measure1]
                    ) * 100

                elif calc_type == "Growth %":

                    df[new_measure] = (
                        df[measure1]
                        .pct_change()
                        * 100
                    )

                elif calc_type == "Running Total":

                    df[new_measure] = (
                        df[measure1]
                        .cumsum()
                    )

                elif calc_type == "Rank":

                    df[new_measure] = (
                        df[measure1]
                        .rank(
                            ascending=False
                        )
                    )

                elif calc_type == "Moving Average":

                    df[new_measure] = (
                        df[measure1]
                        .rolling(window=3)
                        .mean()
                    )

                elif calc_type == "Variance":

                    df[new_measure] = (
                        df[measure1]
                        - df[measure2]
                    )

                elif calc_type == "Variance %":

                    df[new_measure] = (
                        (
                            df[measure1]
                            - df[measure2]
                        )
                        / df[measure2]
                    ) * 100

                elif calc_type == "Contribution %":

                    total = (
                        df[measure1]
                        .sum()
                    )

                    df[new_measure] = (
                        df[measure1]
                        / total
                    ) * 100

                elif calc_type == "Average":

                    avg_value = (
                        df[measure1]
                        .mean()
                    )

                    df[new_measure] = avg_value

                elif calc_type == "Max":

                    max_value = (
                        df[measure1]
                        .max()
                    )

                    df[new_measure] = max_value

                elif calc_type == "Min":

                    min_value = (
                        df[measure1]
                        .min()
                    )

                    df[new_measure] = min_value

                # =====================================================
                # SUCCESS
                # =====================================================

                st.success(
                    f"{new_measure} created successfully"
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
    # PLANNING PAGE
    # =====================================================

    elif menu == "Planning":

        st.subheader("Planning & Data Actions")

        planning_type = st.selectbox(
            "Planning Function",
            [
                "Copy Model",
                "Allocation",
                "Cross Model",
                "Fact Deletion"
            ],
            key="planning_function"
        )

        # =====================================================
        # COPY MODEL
        # =====================================================

        if planning_type == "Copy Model":

            source_measure = st.selectbox(
                "Source Measure",
                measures,
                key="copy_source_measure"
            )

            target_measure = st.text_input(
                "Target Measure Name",
                "Copied_Value",
                key="copy_target_measure"
            )

            increase_percent = st.number_input(
                "Increase %",
                value=0.0,
                key="copy_increase"
            )

            if st.button(
                "Run Copy Model",
                key="copy_model_btn"
            ):

                df[target_measure] = (
                    df[source_measure]
                    * (
                        1
                        + increase_percent / 100
                    )
                ).round(2)

                st.success(
                    "Copy Model Completed"
                )

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
                measures,
                key="allocation_measure"
            )

            allocation_amount = st.number_input(
                "Allocation Amount",
                value=100000.0,
                key="allocation_amount"
            )

            target_column = st.text_input(
                "Allocated Measure Name",
                "Allocated_Value",
                key="allocation_target"
            )

            if st.button(
                "Run Allocation",
                key="allocation_btn"
            ):

                total = (
                    df[allocation_measure]
                    .sum()
                )

                percent = (
                    df[allocation_measure]
                    / total
                )

                df[target_column] = (
                    percent
                    * allocation_amount
                ).round(2)

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
                "Upload Another Model",
                type=["csv", "xlsx"],
                key="cross_model_upload"
            )

            if uploaded_cross is not None:

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
                        common_columns,
                        key="cross_join"
                    )

                    if st.button(
                        "Run Cross Model",
                        key="cross_btn"
                    ):

                        merged_df = pd.merge(
                            df,
                            cross_df,
                            on=join_column,
                            how="left"
                        )

                        st.success(
                            "Cross Model Completed"
                        )

                        st.dataframe(
                            merged_df,
                            use_container_width=True
                        )

        # =====================================================
        # FACT DELETION
        # =====================================================

        elif planning_type == "Fact Deletion":

            delete_measure = st.selectbox(
                "Delete Measure",
                measures,
                key="delete_measure"
            )

            condition = st.selectbox(
                "Condition",
                [
                    "<",
                    ">",
                    "="
                ],
                key="delete_condition"
            )

            threshold = st.number_input(
                "Threshold Value",
                value=1000.0,
                key="delete_threshold"
            )

            if st.button(
                "Run Fact Deletion",
                key="delete_btn"
            ):

                original_rows = len(df)

                if condition == "<":

                    df = df[
                        df[delete_measure]
                        >= threshold
                    ]

                elif condition == ">":

                    df = df[
                        df[delete_measure]
                        <= threshold
                    ]

                elif condition == "=":

                    df = df[
                        df[delete_measure]
                        != threshold
                    ]

                deleted_rows = (
                    original_rows
                    - len(df)
                )

                st.success(
                    f"{deleted_rows} rows deleted"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

    # =====================================================
    # STORY PAGE
    # =====================================================

    elif menu == "Story":

        st.subheader("Story Dashboard")

        # KPI CARDS

        if len(measures) > 0:

            k1, k2, k3, k4 = st.columns(4)

            with k1:
                st.metric(
                    f"Total {measures[0]}",
                    round(df[measures[0]].sum(), 2)
                )

            with k2:
                st.metric(
                    f"Average {measures[0]}",
                    round(df[measures[0]].mean(), 2)
                )

            with k3:
                st.metric(
                    f"Max {measures[0]}",
                    round(df[measures[0]].max(), 2)
                )

            with k4:
                st.metric(
                    f"Min {measures[0]}",
                    round(df[measures[0]].min(), 2)
                )

        # =====================================================
        # FILTERS
        # =====================================================

        filter_df = df.copy()

        if len(dimensions) > 0:

            dimension_filter = st.selectbox(
                "Dimension",
                dimensions,
                key="story_dimension"
            )

            values_filter = st.multiselect(
                "Values",
                filter_df[dimension_filter]
                .astype(str)
                .unique(),
                default=filter_df[dimension_filter]
                .astype(str)
                .unique(),
                key="story_values"
            )

            filter_df = filter_df[
                filter_df[dimension_filter]
                .astype(str)
                .isin(values_filter)
            ]

        # =====================================================
        # CHART BUILDER
        # =====================================================

        c1, c2, c3 = st.columns(3)

        with c1:

            x_axis = st.selectbox(
                "Chart Dimension",
                dimensions,
                key="chart_dimension"
            )

        with c2:

            y_axis = st.selectbox(
                "Chart Measure",
                measures,
                key="chart_measure"
            )

        with c3:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Line",
                    "Pie",
                    "Area"
                ],
                key="chart_type"
            )

        # =====================================================
        # CHARTS
        # =====================================================

        if chart_type == "Bar":

            fig = px.bar(
                filter_df,
                x=x_axis,
                y=y_axis
            )

        elif chart_type == "Line":

            fig = px.line(
                filter_df,
                x=x_axis,
                y=y_axis
            )

        elif chart_type == "Pie":

            fig = px.pie(
                filter_df,
                names=x_axis,
                values=y_axis
            )

        elif chart_type == "Area":

            fig = px.area(
                filter_df,
                x=x_axis,
                y=y_axis
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            filter_df,
            use_container_width=True
        )
# =====================================================
# FORECAST PAGE
# =====================================================

elif menu == "Forecast":

    st.subheader("Forecast Analysis")

    if len(measures) == 0:

        st.warning(
            "No numeric measures available for forecasting."
        )

    else:

        forecast_measure = st.selectbox(
            "Forecast Measure",
            measures,
            key="forecast_measure"
        )

        if forecast_measure not in df.columns:

            st.error(
                f"{forecast_measure} not found in dataframe."
            )

        else:

            # Convert safely
            df[forecast_measure] = pd.to_numeric(
                df[forecast_measure],
                errors="coerce"
            )

            forecast_percent = st.slider(
                "Forecast Increase %",
                1,
                100,
                10,
                key="forecast_slider"
            )

            forecast_df = df.copy()

            forecast_df["Forecast"] = (
                forecast_df[forecast_measure]
                * (
                    1
                    + forecast_percent / 100
                )
            ).round(2)

            st.success(
                f"Forecast created for {forecast_measure}"
            )

            # ---------------- TABLE ----------------

            st.dataframe(
                forecast_df,
                use_container_width=True
            )

            # ---------------- CHART ----------------

            try:

                fig = px.line(
                    forecast_df,
                    y=[
                        forecast_measure,
                        "Forecast"
                    ],
                    title=f"{forecast_measure} Forecast"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"Chart Error: {e}"
                )
   
