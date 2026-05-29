import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Advanced SAC Planning App",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------- TITLE ----------------
st.title("📊 SAC Style Planning & Calculations")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# ---------------- MAIN ----------------
if uploaded_file is not None:

    # ---------------- READ FILE ----------------
    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:
        st.error(f"File Error: {e}")
        st.stop()

    # ---------------- DETECT MEASURES ----------------
    measures = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):
            measures.append(col)

    # ---------------- DATASET ----------------
    st.subheader("Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ---------------- CALCULATED MEASURE SECTION ----------------
    st.subheader("Create Calculated Measure")

    # ---------------- CALCULATIONS ----------------
    calculation_types = [

        # Basic
        "Addition",
        "Subtraction",
        "Multiplication",
        "Division",

        # Percentage
        "Profit %",
        "Growth %",
        "Percentage Contribution",

        # Aggregation
        "Average",
        "Sum",
        "Minimum",
        "Maximum",
        "Count",

        # Running
        "Running Total",
        "Cumulative Average",

        # Ranking
        "Rank",
        "Dense Rank",

        # Statistics
        "Standard Deviation",
        "Variance",
        "Z-Score",

        # Time
        "Moving Average",
        "Rolling Sum",

        # Window
        "Lag",
        "Lead",

        # Conditional
        "High/Low Category",

        # Finance
        "Margin %",
        "Tax Calculation",
        "Discount Calculation",

        # Analytics
        "Percentile",
        "Normalized Score",

        # ---------------- PLANNING ----------------
        "Allocation",
        "Fact Deletion",
        "Top Down Allocation",
        "Bottom Up Allocation",
        "Spread Value",
        "Forecast Increase %",
        "Copy Value"
    ]

    col1, col2, col3 = st.columns(3)

    # ---------------- MEASURE 1 ----------------
    with col1:

        measure1 = st.selectbox(
            "Select Measure 1",
            measures
        )

    # ---------------- CALCULATION TYPE ----------------
    with col2:

        calc_type = st.selectbox(
            "Calculation Type",
            calculation_types
        )

    # ---------------- MEASURE 2 ----------------
    with col3:

        calculations_without_measure2 = [

            "Running Total",
            "Average",
            "Growth %",
            "Sum",
            "Minimum",
            "Maximum",
            "Count",
            "Cumulative Average",
            "Rank",
            "Dense Rank",
            "Standard Deviation",
            "Variance",
            "Z-Score",
            "Moving Average",
            "Rolling Sum",
            "Lag",
            "Lead",
            "High/Low Category",
            "Tax Calculation",
            "Discount Calculation",
            "Percentile",
            "Normalized Score",

            # Planning
            "Allocation",
            "Fact Deletion",
            "Top Down Allocation",
            "Bottom Up Allocation",
            "Spread Value",
            "Forecast Increase %",
            "Copy Value",
            "Percentage Contribution"
        ]

        if calc_type in calculations_without_measure2:

            measure2 = None
            st.info("Second measure not needed")

        else:

            measure2 = st.selectbox(
                "Select Measure 2",
                measures
            )

    # ---------------- NEW COLUMN ----------------
    new_measure_name = st.text_input(
        "Calculated Measure Name",
        "Calculated_Measure"
    )

    # ---------------- CREATE BUTTON ----------------
    if st.button("Create Calculated Measure"):

        try:

            # Convert numeric
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
            # BASIC CALCULATIONS
            # =====================================================

            if calc_type == "Addition":

                df[new_measure_name] = (
                    df[measure1]
                    + df[measure2]
                )

            elif calc_type == "Subtraction":

                df[new_measure_name] = (
                    df[measure1]
                    - df[measure2]
                )

            elif calc_type == "Multiplication":

                df[new_measure_name] = (
                    df[measure1]
                    * df[measure2]
                )

            elif calc_type == "Division":

                df[new_measure_name] = (
                    df[measure1]
                    / df[measure2]
                ).replace(
                    [np.inf, -np.inf],
                    np.nan
                )

            # =====================================================
            # PERCENTAGE
            # =====================================================

            elif calc_type == "Profit %":

                df[new_measure_name] = (
                    (
                        df[measure1]
                        - df[measure2]
                    )
                    / df[measure1]
                ) * 100

            elif calc_type == "Growth %":

                df[new_measure_name] = (
                    df[measure1]
                    .pct_change()
                    * 100
                )

            elif calc_type == "Percentage Contribution":

                total = df[measure1].sum()

                df[new_measure_name] = (
                    df[measure1]
                    / total
                ) * 100

            # =====================================================
            # AGGREGATION
            # =====================================================

            elif calc_type == "Average":

                avg_value = (
                    df[measure1]
                    .mean()
                )

                df[new_measure_name] = avg_value

            elif calc_type == "Sum":

                total = (
                    df[measure1]
                    .sum()
                )

                df[new_measure_name] = total

            elif calc_type == "Minimum":

                min_value = (
                    df[measure1]
                    .min()
                )

                df[new_measure_name] = min_value

            elif calc_type == "Maximum":

                max_value = (
                    df[measure1]
                    .max()
                )

                df[new_measure_name] = max_value

            elif calc_type == "Count":

                count_value = (
                    df[measure1]
                    .count()
                )

                df[new_measure_name] = count_value

            # =====================================================
            # RUNNING
            # =====================================================

            elif calc_type == "Running Total":

                df[new_measure_name] = (
                    df[measure1]
                    .cumsum()
                )

            elif calc_type == "Cumulative Average":

                df[new_measure_name] = (
                    df[measure1]
                    .expanding()
                    .mean()
                )

            # =====================================================
            # RANKING
            # =====================================================

            elif calc_type == "Rank":

                df[new_measure_name] = (
                    df[measure1]
                    .rank(
                        ascending=False
                    )
                )

            elif calc_type == "Dense Rank":

                df[new_measure_name] = (
                    df[measure1]
                    .rank(
                        method="dense",
                        ascending=False
                    )
                )

            # =====================================================
            # STATISTICS
            # =====================================================

            elif calc_type == "Standard Deviation":

                std_value = (
                    df[measure1]
                    .std()
                )

                df[new_measure_name] = std_value

            elif calc_type == "Variance":

                var_value = (
                    df[measure1]
                    .var()
                )

                df[new_measure_name] = var_value

            elif calc_type == "Z-Score":

                mean = (
                    df[measure1]
                    .mean()
                )

                std = (
                    df[measure1]
                    .std()
                )

                df[new_measure_name] = (
                    (
                        df[measure1]
                        - mean
                    )
                    / std
                )

            # =====================================================
            # TIME
            # =====================================================

            elif calc_type == "Moving Average":

                df[new_measure_name] = (
                    df[measure1]
                    .rolling(window=3)
                    .mean()
                )

            elif calc_type == "Rolling Sum":

                df[new_measure_name] = (
                    df[measure1]
                    .rolling(window=3)
                    .sum()
                )

            # =====================================================
            # WINDOW FUNCTIONS
            # =====================================================

            elif calc_type == "Lag":

                df[new_measure_name] = (
                    df[measure1]
                    .shift(1)
                )

            elif calc_type == "Lead":

                df[new_measure_name] = (
                    df[measure1]
                    .shift(-1)
                )

            # =====================================================
            # CONDITIONAL
            # =====================================================

            elif calc_type == "High/Low Category":

                avg = (
                    df[measure1]
                    .mean()
                )

                df[new_measure_name] = np.where(
                    df[measure1] > avg,
                    "High",
                    "Low"
                )

            # =====================================================
            # FINANCE
            # =====================================================

            elif calc_type == "Margin %":

                df[new_measure_name] = (
                    (
                        df[measure1]
                        - df[measure2]
                    )
                    / df[measure1]
                ) * 100

            elif calc_type == "Tax Calculation":

                df[new_measure_name] = (
                    df[measure1]
                    * 0.18
                )

            elif calc_type == "Discount Calculation":

                df[new_measure_name] = (
                    df[measure1]
                    * 0.10
                )

            # =====================================================
            # ANALYTICS
            # =====================================================

            elif calc_type == "Percentile":

                df[new_measure_name] = (
                    df[measure1]
                    .rank(pct=True)
                    * 100
                )

            elif calc_type == "Normalized Score":

                min_val = (
                    df[measure1]
                    .min()
                )

                max_val = (
                    df[measure1]
                    .max()
                )

                df[new_measure_name] = (
                    (
                        df[measure1]
                        - min_val
                    )
                    /
                    (
                        max_val
                        - min_val
                    )
                )

            # =====================================================
            # PLANNING
            # =====================================================

            elif calc_type == "Allocation":

                total_value = (
                    df[measure1]
                    .sum()
                )

                percentage = (
                    df[measure1]
                    / total_value
                )

                allocation_amount = st.number_input(
                    "Allocation Amount",
                    value=100000.0
                )

                df[new_measure_name] = (
                    percentage
                    * allocation_amount
                ).round(2)

            elif calc_type == "Fact Deletion":

                threshold = st.number_input(
                    "Delete rows below value",
                    value=1000.0
                )

                df = df[
                    df[measure1]
                    >= threshold
                ]

                st.warning(
                    "Rows deleted based on threshold"
                )

                df[new_measure_name] = "Remaining"

            elif calc_type == "Top Down Allocation":

                total_budget = st.number_input(
                    "Total Budget",
                    value=50000.0
                )

                row_count = len(df)

                df[new_measure_name] = (
                    total_budget / row_count
                )

            elif calc_type == "Bottom Up Allocation":

                total = (
                    df[measure1]
                    .sum()
                )

                df[new_measure_name] = total

            elif calc_type == "Spread Value":

                spread_amount = st.number_input(
                    "Spread Amount",
                    value=12000.0
                )

                periods = st.number_input(
                    "Number of Periods",
                    value=12
                )

                spread_value = (
                    spread_amount / periods
                )

                df[new_measure_name] = spread_value

            elif calc_type == "Forecast Increase %":

                increase_percent = st.number_input(
                    "Increase %",
                    value=10.0
                )

                df[new_measure_name] = (
                    df[measure1]
                    * (
                        1
                        + increase_percent / 100
                    )
                ).round(2)

            elif calc_type == "Copy Value":

                df[new_measure_name] = (
                    df[measure1]
                )

            # =====================================================
            # SUCCESS
            # =====================================================

            st.success(
                f"{new_measure_name} created successfully"
            )

            st.subheader("Updated Dataset")

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(
                f"Calculation Error: {e}"
            )

else:
    st.info("Upload CSV or Excel File")
