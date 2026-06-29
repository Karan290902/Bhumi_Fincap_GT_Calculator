# ============================================
# IMPORT LIBRARIES
# ============================================

import streamlit as st
import pandas as pd
import numpy as np

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Insurance Premium Calculator",
    page_icon="💰",
    layout="wide"
)

# ============================================
# TITLE
# ============================================

st.title("💰 Group Term Life Insurance Premium Calculator")

st.markdown(
    "Upload any insurance Excel file for premium calculation"
)

# ============================================
# QUICK PREMIUM CALCULATOR
# ============================================

st.divider()

st.subheader("⚡ Quick Premium Calculator")

st.write("Calculate premium instantly without uploading an Excel file.")

QUICK_RATE = 368.64          # Inclusive of GST
QUICK_GST = 0.18

col1, col2 = st.columns([3,1])

with col1:

    quick_sum_assured = st.number_input(
        "Enter Sum Assured (₹)",
        min_value=0,
        value=1000000,
        step=100000,
        key="quick_sa"
    )

with col2:

    st.write("")
    st.write("")

    calculate = st.button("Calculate Premium")

if calculate:

    total_premium = (

        (quick_sum_assured / 100000)

        *

        QUICK_RATE

    )

    premium_excl = (

        total_premium

        /

        (1 + QUICK_GST)

    )

    gst_amount = (

        total_premium

        -

        premium_excl

    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Premium Excl GST",
            f"₹ {premium_excl:,.2f}"
        )

    with c2:

        st.metric(
            "GST Amount",
            f"₹ {gst_amount:,.2f}"
        )

    with c3:

        st.metric(
            "Total Premium",
            f"₹ {total_premium:,.2f}"
        )

st.divider()

# ============================================
# SETTINGS
# ============================================

RATE_PER_LAKH = 368.64

GST_RATE = 0.18

# ============================================
# FILE UPLOAD
# ============================================

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

# ============================================
# PROCESS FILE
# ============================================

if uploaded_file is not None:

    try:

        # ============================================
        # READ FILE
        # ============================================

        df = pd.read_excel(uploaded_file)

        # ============================================
        # CLEAN COLUMN NAMES
        # ============================================

        df.columns = df.columns.str.strip()

        # ============================================
        # SHOW ORIGINAL DATA
        # ============================================

        st.subheader("Uploaded Data")

        st.dataframe(df.head())

        # ============================================
        # HANDLE MISSING COLUMNS
        # ============================================

        required_columns = [

            'Loan Account No.',

            'Name of Primary Loan borrower',

            'Mobile No',

            'Sum Assured'

        ]

        for col in required_columns:

            if col not in df.columns:

                df[col] = ""

        # ============================================
        # CLEAN SUM ASSURED
        # ============================================

        df['Sum Assured'] = pd.to_numeric(

            df['Sum Assured'],

            errors='coerce'

        ).fillna(0)

        # ============================================
        # OPTIONAL AGE COLUMN
        # ============================================

        if 'MAIN MEMBER AGE' not in df.columns:

            df['MAIN MEMBER AGE'] = 0

        # ============================================
        # OPTIONAL LOAN COLUMN
        # ============================================

        if 'Loan Outstanding Amount' not in df.columns:

            df['Loan Outstanding Amount'] = 0
        # ============================================
        # PREMIUM CALCULATION
        # ============================================

        df['Premium Excl GST'] = (

            (df['Sum Assured'] / 100000)

            *

            RATE_PER_LAKH

        )

        # ============================================
        # GST CALCULATION
        # ============================================

        df['Premium + GST'] = (

            df['Premium Excl GST']

            +

            (df['Premium Excl GST'] * GST_RATE)

        )

        # ============================================
        # FINAL OUTPUT
        # ============================================

        output_columns = [

            'Loan Account No.',

            'Name of Primary Loan borrower',

            'Mobile No',

            'MAIN MEMBER AGE',

            'Sum Assured',

            'Premium Excl GST',

            'Premium + GST'

        ]

        final_df = df[output_columns]

        # ============================================
        # DASHBOARD
        # ============================================

        st.subheader("Portfolio Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Members",
                len(final_df)
            )

        with col2:

            st.metric(
                "Total Sum Assured",
                f"₹ {final_df['Sum Assured'].sum():,.0f}"
            )

        with col3:

            st.metric(
                "Total Premium",
                f"₹ {final_df['Premium + GST'].sum():,.2f}"
            )

        # ============================================
        # SHOW OUTPUT
        # ============================================

        st.subheader("Premium Calculation Output")

        st.dataframe(

            final_df,

            use_container_width=True

        )

        # ============================================
        # DOWNLOAD BUTTON
        # ============================================

        output_file = "Premium_Output.xlsx"

        final_df.to_excel(

            output_file,

            index=False

        )

        with open(output_file, "rb") as file:

            st.download_button(
                label="⬇ Download Output Excel",
                data=file,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:

        st.error(f"Error: {e}")
