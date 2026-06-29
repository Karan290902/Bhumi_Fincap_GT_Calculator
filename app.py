import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Insurance Premium Calculator",
    page_icon="💰",
    layout="wide"
)

# ============================================
# SETTINGS
# ============================================

RATE_PER_LAKH = 435      # Inclusive of GST
GST_RATE = 0.18

# ============================================
# TITLE
# ============================================

st.title("💰 Group Term Life Insurance Premium Calculator")

st.markdown(
    """
Calculate premium instantly or upload an Excel file for bulk premium calculation.

**Rate:** ₹435 per lakh (Inclusive of GST)
"""
)

# ============================================
# QUICK PREMIUM CALCULATOR
# ============================================

st.subheader("⚡ Quick Premium Calculator")

sum_assured = st.number_input(
    "Enter Sum Assured (₹)",
    min_value=0.0,
    value=1000000.0,
    step=100000.0
)

if st.button("Calculate Premium"):

    total_premium = (
        (sum_assured / 100000)
        * RATE_PER_LAKH
    )

    premium_excl = (
        total_premium
        / (1 + GST_RATE)
    )

    gst_amount = (
        total_premium
        - premium_excl
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
            "Total Premium (Incl GST)",
            f"₹ {total_premium:,.2f}"
        )

st.divider()

# ============================================
# BULK PREMIUM CALCULATOR
# ============================================

st.subheader("📂 Bulk Premium Calculator")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

        # ============================================
        # READ EXCEL
        # ============================================

        df = pd.read_excel(uploaded_file)

        df.columns = df.columns.str.strip()

        st.subheader("Uploaded Data")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        # ============================================
        # DETECT SUM ASSURED COLUMN
        # ============================================

        possible_columns = [

            "Sum Assured",

            "Sum Insured",

            "SI",

            "SA",

            "Coverage",

            "Cover Amount"

        ]

        sum_assured_column = None

        for col in possible_columns:

            if col in df.columns:

                sum_assured_column = col

                break

        if sum_assured_column is None:

            st.error(
                "No Sum Assured column found.\n\nAccepted names:\n\nSum Assured\nSum Insured\nSI\nSA\nCoverage\nCover Amount"
            )

            st.stop()

        df[sum_assured_column] = pd.to_numeric(
            df[sum_assured_column],
            errors="coerce"
        ).fillna(0)
                # ============================================
        # PREMIUM CALCULATIONS
        # ============================================

        # Total Premium (Inclusive of GST)
        df["Premium + GST"] = (

            (df[sum_assured_column] / 100000)

            *

            RATE_PER_LAKH

        )

        # Premium Excluding GST

        df["Premium Excl GST"] = (

            df["Premium + GST"]

            /

            (1 + GST_RATE)

        )

        # GST Amount

        df["GST Amount"] = (

            df["Premium + GST"]

            -

            df["Premium Excl GST"]

        )

        # ============================================
        # KEEP ORIGINAL EXCEL FORMAT
        # ============================================

        final_df = df.copy()

        # ============================================
        # PORTFOLIO SUMMARY
        # ============================================

        st.subheader("Portfolio Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Total Records",

                len(final_df)

            )

        with col2:

            st.metric(

                "Total Sum Assured",

                f"₹ {final_df[sum_assured_column].sum():,.0f}"

            )

        with col3:

            st.metric(

                "Total Premium",

                f"₹ {final_df['Premium + GST'].sum():,.2f}"

            )

        # ============================================
        # OUTPUT TABLE
        # ============================================

        st.subheader("Premium Calculation Output")

        st.dataframe(

            final_df,

            use_container_width=True

        )

        # ============================================
        # DOWNLOAD OUTPUT
        # ============================================

        output_file = "Premium_Output.xlsx"

        with pd.ExcelWriter(

            output_file,

            engine="openpyxl"

        ) as writer:

            final_df.to_excel(

                writer,

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

        st.error(

            f"Error: {e}"

        )
