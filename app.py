import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Auto Calculated Measures",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 Auto Calculated Measures")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# ---------------- MAIN ----------------
if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    # ---------------- DETECT MEASURES ----------------
    measures = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):
            measures.append(col)

    # ---------------- SHOW DATA ----------------
    st.subheader("Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ---------------- CALCULATED MEASURE ----------------
    st.subheader("Create Calculated Measure")

    # Calculation Types
    calculation_types = [
        "Addition",
        "Subtraction",
        "Multiplication",
        "Division",
        "Profit %",
        "Running Total",
        "Average",
        "Rank",
        "Growth %"
    ]

    col1, col2, col3 = st.columns(3)

    # Measure 1
    with col1:
        measure1 = st.selectbox(
            "Select Measure 1",
            measures
        )

    # Calculation
    with col2:
        calc_type = st.selectbox(
            "Calculation Type",
            calculation_types
        )

    # Measure 2
    with col3:

        # Some calculations don't need Measure2
        if calc_type in [
            "Running Total",
            "Average",
            "Rank",
            "Growth %"
        ]:
            measure2 = None
            st.write("No second measure needed")

        else:
            measure2 = st.selectbox(
                "Select Measure 2",
                measures
            )

    # New Column Name
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

            # ---------------- CALCULATIONS ----------------

            # Addition
            if calc_type == "Addition":

                df[new_measure_name] = (
                    df[measure1]
                    + df[measure2]
                )

            # Subtraction
            elif calc_type == "Subtraction":

                df[new_measure_name] = (
                    df[measure1]
                    - df[measure2]
                )

            # Multiplication
            elif calc_type == "Multiplication":

                df[new_measure_name] = (
                    df[measure1]
                    * df[measure2]
                )

            # Division
            elif calc_type == "Division":

                df[new_measure_name] = (
                    df[measure1]
                    / df[measure2]
                ).replace(
                    [np.inf, -np.inf],
                    np.nan
                )

            # Profit %
            elif calc_type == "Profit %":

                df[new_measure_name] = (
                    (
                        df[measure1]
                        - df[measure2]
                    )
                    / df[measure1]
                ) * 100

            # Running Total
            elif calc_type == "Running Total":

                df[new_measure_name] = (
                    df[measure1]
                    .cumsum()
                )

            # Average
            elif calc_type == "Average":

                avg_value = (
                    df[measure1]
                    .mean()
                )

                df[new_measure_name] = avg_value

            # Rank
            elif calc_type == "Rank":

                df[new_measure_name] = (
                    df[measure1]
                    .rank(
                        ascending=False
                    )
                )

            # Growth %
            elif calc_type == "Growth %":

                df[new_measure_name] = (
                    df[measure1]
                    .pct_change()
                    * 100
                )

            # ---------------- SUCCESS ----------------
            st.success(
                f"{new_measure_name} created successfully"
            )

            # Show updated table
            st.subheader("Updated Dataset")

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Calculation Error: {e}")

else:
    st.info("Upload CSV or Excel File")
