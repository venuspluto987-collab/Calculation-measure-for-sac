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
        New_Analytic_Model
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
    # AUTO DETECT
    # =====================================================

    measures = []
    dimensions = []
    date_columns = []

    for col in df.columns:

        # Date
        if "date" in col.lower():

            date_columns.append(col)
            dimensions.append(col)

        # Numeric
        elif (
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
        # DATA TABLE
        # =====================================================

        st.subheader("Preview Data")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

    # =====================================================
    # STORY PAGE
    # =====================================================

    elif menu == "Story":

        st.subheader("Story Dashboard")

        # =====================================================
        # KPI CARDS
        # =====================================================

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        if len(measures) > 0:

            with kpi1:

                total = round(
                    df[measures[0]].sum(),
                    2
                )

                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">
                            Total {measures[0]}
                        </div>
                        <div class="kpi-value">
                            {total}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if len(measures) > 1:

            with kpi2:

                avg = round(
                    df[measures[1]].mean(),
                    2
                )

                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">
                            Average {measures[1]}
                        </div>
                        <div class="kpi-value">
                            {avg}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if len(measures) > 0:

            with kpi3:

                max_value = round(
                    df[measures[0]].max(),
                    2
                )

                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">
                            Max {measures[0]}
                        </div>
                        <div class="kpi-value">
                            {max_value}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if len(measures) > 0:

            with kpi4:

                min_value = round(
                    df[measures[0]].min(),
                    2
                )

                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">
                            Min {measures[0]}
                        </div>
                        <div class="kpi-value">
                            {min_value}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # =====================================================
        # FILTERS
        # =====================================================

        st.subheader("Filters")

        filter_col1, filter_col2 = st.columns(2)

        filtered_df = df.copy()

        if len(dimensions) > 0:

            with filter_col1:

                selected_dimension = st.selectbox(
                    "Select Dimension",
                    dimensions
                )

            with filter_col2:

                unique_values = df[
                    selected_dimension
                ].astype(str).unique()

                selected_values = st.multiselect(
                    "Select Values",
                    unique_values,
                    default=unique_values
                )

            filtered_df = filtered_df[
                filtered_df[selected_dimension]
                .astype(str)
                .isin(selected_values)
            ]

        # =====================================================
        # CHART BUILDER
        # =====================================================

        st.subheader("Chart Builder")

        chart_col1, chart_col2, chart_col3 = st.columns(3)

        with chart_col1:

            x_axis = st.selectbox(
                "Dimension",
                dimensions
            )

        with chart_col2:

            y_axis = st.selectbox(
                "Measure",
                measures
            )

        with chart_col3:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Line",
                    "Pie",
                    "Area"
                ]
            )

        # ---------------- CHARTS ----------------

        fig = None

        if chart_type == "Bar":

            fig = px.bar(
                filtered_df,
                x=x_axis,
                y=y_axis
            )

        elif chart_type == "Line":

            fig = px.line(
                filtered_df,
                x=x_axis,
                y=y_axis
            )

        elif chart_type == "Pie":

            fig = px.pie(
                filtered_df,
                names=x_axis,
                values=y_axis
            )

        elif chart_type == "Area":

            fig = px.area(
                filtered_df,
                x=x_axis,
                y=y_axis
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================================
        # TABLE
        # =====================================================

        st.subheader("Story Table")

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    # =====================================================
    # PLANNING PAGE
    # =====================================================

    elif menu == "Planning":

        st.subheader("Planning & Calculations")

        calc_types = [

            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
            "Profit %",
            "Growth %",
            "Running Total",
            "Rank",
            "Moving Average",
            "Allocation",
            "Forecast Increase %",
            "Copy Value"
        ]

        c1, c2, c3 = st.columns(3)

        with c1:

            measure1 = st.selectbox(
                "Measure 1",
                measures
            )

        with c2:

            calc_type = st.selectbox(
                "Calculation",
                calc_types
            )

        with c3:

            if calc_type in [
                "Running Total",
                "Growth %",
                "Rank",
                "Moving Average",
                "Allocation",
                "Forecast Increase %",
                "Copy Value"
            ]:

                measure2 = None
                st.info("No second measure needed")

            else:

                measure2 = st.selectbox(
                    "Measure 2",
                    measures
                )

        new_measure = st.text_input(
            "Calculated Measure Name",
            "Calculated_Measure"
        )

        # =====================================================
        # CREATE CALCULATION
        # =====================================================

        if st.button("Create Calculation"):

            try:

                # Numeric Conversion
                df[measure1] = pd.to_numeric(
                    df[measure1],
                    errors="coerce"
                )

                if measure2:
                    df[measure2] = pd.to_numeric(
                        df[measure2],
                        errors="coerce"
                    )

                # ---------------- BASIC ----------------

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

                # ---------------- ADVANCED ----------------

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

                # ---------------- PLANNING ----------------

                elif calc_type == "Allocation":

                    allocation_amount = st.number_input(
                        "Allocation Amount",
                        value=100000.0
                    )

                    total = (
                        df[measure1]
                        .sum()
                    )

                    percent = (
                        df[measure1]
                        / total
                    )

                    df[new_measure] = (
                        percent
                        * allocation_amount
                    ).round(2)

                elif calc_type == "Forecast Increase %":

                    increase_percent = st.number_input(
                        "Forecast Increase %",
                        value=10.0
                    )

                    df[new_measure] = (
                        df[measure1]
                        * (
                            1
                            + increase_percent / 100
                        )
                    )

                elif calc_type == "Copy Value":

                    df[new_measure] = (
                        df[measure1]
                    )

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
    # FORECAST PAGE
    # =====================================================

    elif menu == "Forecast":

        st.subheader("Forecast Analysis")

        measure = st.selectbox(
            "Select Measure",
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
            forecast_df[measure]
            * (
                1 + forecast_percent / 100
            )
        )

        fig = px.line(
            forecast_df,
            y=[measure, "Forecast"]
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
