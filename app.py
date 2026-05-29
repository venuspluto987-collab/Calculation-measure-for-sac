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
    # EMPTY DATA CHECK
    # =====================================================

    if df.empty:

        st.warning("Uploaded file is empty")
        st.stop()

    # =====================================================
    # AUTO DETECT DIMENSIONS / MEASURES
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

        # =====================================================
        # DIMENSIONS
        # =====================================================

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

            if len(dimensions) > 0:

                for d in dimensions:

                    st.markdown(
                        f"""
                        <div class="dimension-item">
                            {d}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info("No dimensions found")

            st.markdown("</div>", unsafe_allow_html=True)

        # =====================================================
        # MEASURES
        # =====================================================

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

            if len(measures) > 0:

                for m in measures:

                    st.markdown(
                        f"""
                        <div class="measure-item">
                            {m}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info("No measures found")

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
# MAIN DATAFRAME
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
    # AUTO DETECT DIMENSIONS / MEASURES
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

        # =====================================================
        # DIMENSIONS
        # =====================================================

        with col1:

            st.markdown("### Dimensions")

            for d in dimensions:

                st.write("•", d)

        # =====================================================
        # MEASURES
        # =====================================================

        with col2:

            st.markdown("### Measures")

            for m in measures:

                st.write("•", m)

        # =====================================================
        # PREVIEW
        # =====================================================

        st.subheader("Preview Data")

        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )

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

        # =====================================================
        # IF CONDITION
        # =====================================================

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

        # =====================================================
        # CUSTOM FORMULA
        # =====================================================

        formula = ""

        if calc_type == "Custom Formula":

            formula = st.text_input(
                "Formula Example: Sales * Quantity"
            )

        # =====================================================
        # RUN CALCULATION
        # =====================================================

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

                # =====================================================
                # ROUND
                # =====================================================

                df[calc_name] = (
                    df[calc_name]
                    .round(2)
                )

                # =====================================================
                # SAVE SESSION
                # =====================================================

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

        # =====================================================
        # CHECKS
        # =====================================================

        if len(measures) == 0:

            st.warning(
                "No numeric measures found in dataset"
            )

            st.stop()

        if len(dimensions) == 0:

            st.warning(
                "No dimensions found in dataset"
            )

            st.stop()

        # =====================================================
        # KPI CARDS
        # =====================================================

        k1, k2, k3, k4 = st.columns(4)

        with k1:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">
                        Total {measures[0]}
                    </div>
                    <div class="kpi-value">
                        {round(df[measures[0]].sum(),2)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k2:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">
                        Average {measures[0]}
                    </div>
                    <div class="kpi-value">
                        {round(df[measures[0]].mean(),2)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k3:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">
                        Max {measures[0]}
                    </div>
                    <div class="kpi-value">
                        {round(df[measures[0]].max(),2)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k4:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">
                        Min {measures[0]}
                    </div>
                    <div class="kpi-value">
                        {round(df[measures[0]].min(),2)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =====================================================
        # FILTERS
        # =====================================================

        st.subheader("Filters")

        filter_df = df.copy()

        f1, f2 = st.columns(2)

        with f1:

            selected_dimension = st.selectbox(
                "Dimension",
                dimensions
            )

        with f2:

            selected_values = st.multiselect(
                "Values",
                filter_df[selected_dimension]
                .astype(str)
                .dropna()
                .unique(),
                default=filter_df[selected_dimension]
                .astype(str)
                .dropna()
                .unique()
            )

        filter_df = filter_df[
            filter_df[selected_dimension]
            .astype(str)
            .isin(selected_values)
        ]

        # =====================================================
        # CHART BUILDER
        # =====================================================

        st.subheader("Chart Builder")

        c1, c2, c3 = st.columns(3)

        with c1:

            x_axis = st.selectbox(
                "X Axis",
                dimensions
            )

        with c2:

            y_axis = st.selectbox(
                "Y Axis",
                measures
            )

        with c3:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Line",
                    "Pie",
                    "Area"
                ]
            )

        # =====================================================
        # CHARTS
        # =====================================================

        fig = None

        try:

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

        except Exception as e:

            st.error(f"Chart Error: {e}")

        # =====================================================
        # STORY TABLE
        # =====================================================

        st.subheader("Story Table")

        st.dataframe(
            filter_df,
            use_container_width=True
        )

    # =====================================================
    # PLANNING PAGE
    # =====================================================

    elif menu == "Planning":

        st.subheader("Planning & Data Actions")

        if len(measures) == 0:

            st.warning(
                "No numeric measures found"
            )

            st.stop()

        planning_type = st.selectbox(
            "Planning Function",
            [
                "Copy Model",
                "Allocation",
                "Cross Model",
                "Fact Deletion"
            ]
        )

        # =====================================================
        # COPY MODEL
        # =====================================================

        if planning_type == "Copy Model":

            source_measure = st.selectbox(
                "Source Measure",
                measures
            )

            target_measure = st.text_input(
                "Target Measure Name",
                "Copied_Value"
            )

            increase_percent = st.number_input(
                "Increase %",
                value=0.0
            )

            if st.button("Run Copy Model"):

                try:

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

                except Exception as e:

                    st.error(f"Error: {e}")

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
                "Allocated Measure Name",
                "Allocated_Value"
            )

            if st.button("Run Allocation"):

                try:

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

                except Exception as e:

                    st.error(f"Error: {e}")

        # =====================================================
        # CROSS MODEL
        # =====================================================

        elif planning_type == "Cross Model":

            uploaded_cross = st.file_uploader(
                "Upload Another Model",
                type=["csv", "xlsx"],
                key="crossmodel"
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

                    st.subheader(
                        "Cross Model Preview"
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

                        if st.button(
                            "Run Cross Model"
                        ):

                            merged_df = pd.merge(
                                df,
                                cross_df,
                                on=join_column,
                                how="left"
                            )

                            st.success(
                                "Cross Model Merge Completed"
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

                    st.error(f"Error: {e}")

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
                    "="
                ]
            )

            threshold = st.number_input(
                "Threshold Value",
                value=1000.0
            )

            if st.button(
                "Run Fact Deletion"
            ):

                try:

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

                except Exception as e:

                    st.error(f"Error: {e}")

    # =====================================================
    # FORECAST PAGE
    # =====================================================

    elif menu == "Forecast":

        st.subheader("Forecast Analysis")

        if len(measures) == 0:

            st.warning(
                "No numeric measures found"
            )

            st.stop()

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

        fig = px.line(
            forecast_df,
            y=[
                forecast_measure,
                "Forecast"
            ]
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
