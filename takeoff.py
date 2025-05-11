import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Construction Cost Data Filter", layout="wide")
st.title("📊 Construction Cost Data Filter")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read Excel
        df = pd.read_excel(uploaded_file)

        # Rebuild your column mapping
        df['Title'] = df.apply(lambda row: f"{row['#']} - {row['Desc']}", axis=1)
        df['Description'] = df['Activity']
        df['Parent Group'] = df['Group Description']
        df['Parent Group Description'] = ""
        df['Subgroup'] = ""
        df['Subgroup Description'] = ""
        df['Cost Code'] = df['Owner']
        df['Quantity'] = df['Qty']
        df['Unit'] = df['Unit']
        df['Unit Cost'] = df['Unit Cost']
        df['Cost Type'] = df['Coverage']
        df['Total Cost'] = df['ACV']
        df['Markup Percentage'] = 21  # Business rule assumption
        df['Line Item Type'] = df['Activity']
        df['Internal Notes'] = df['Note 1']

        # Output structure
        final_columns = [
            'Title', 'Description', 'Parent Group', 'Parent Group Description', 'Subgroup', 'Subgroup Description',
            'Cost Code', 'Quantity', 'Unit', 'Unit Cost', 'Cost Type', 'Total Cost',
            'Markup Percentage', 'Line Item Type', 'Internal Notes'
        ]
        final_df = df[final_columns]

        st.success("✅ File processed successfully!")
        st.dataframe(final_df)

        # Excel export
        buffer = BytesIO()
        final_df.to_excel(buffer, index=False)
        st.download_button(
            label="📥 Download Processed Excel",
            data=buffer.getvalue(),
            file_name="filtered_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
