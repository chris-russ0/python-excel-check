import streamlit as st
import pandas as pd
import os

def compare_codes(df1, df2, column1, column2):
    """
    Compare codes between two DataFrames
    
    :param df1: First DataFrame
    :param df2: Second DataFrame
    :param column1: Column name in first DataFrame
    :param column2: Column name in second DataFrame
    :return: Set of missing codes and total count
    """
    try:
        # Convert columns to string to handle various data types
        codici1 = set(df1[column1].dropna().astype(str))
        codici2 = set(df2[column2].dropna().astype(str))

        # Find missing codes
        mancanti = codici1 - codici2

        return mancanti, len(mancanti)
    
    except KeyError as e:
        st.error(f"Column not found: {e}")
        return set(), 0
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return set(), 0

def main():
    # Page configuration
    st.set_page_config(
        page_title="Code Comparison Tool",
        page_icon="🔍",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("📊 Excel Code Comparison Tool")
    st.markdown("Compare codes between two Excel files and identify missing values.")

    # Sidebar for configuration
    st.sidebar.header("📝 Configuration")

    # File uploaders
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("First Excel File")
        file1 = st.file_uploader(
            "Upload First Excel File", 
            type=['xlsx', 'xls'],
            key="file1"
        )
        column1 = st.text_input(
            "Column Name for First File", 
            key="column1"
        )

    with col2:
        st.subheader("Second Excel File")
        file2 = st.file_uploader(
            "Upload Second Excel File", 
            type=['xlsx', 'xls'],
            key="file2"
        )
        column2 = st.text_input(
            "Column Name for Second File", 
            key="column2"
        )

    # Comparison button
    if st.button("Compare Files", type="primary"):
        # Validate inputs
        if not file1 or not file2:
            st.warning("Please upload both Excel files.")
            return

        if not column1 or not column2:
            st.warning("Please specify column names for both files.")
            return

        try:
            # Read Excel files
            df1 = pd.read_excel(file1)
            df2 = pd.read_excel(file2)

            # Validate columns
            if column1 not in df1.columns:
                st.error(f"Column '{column1}' not found in first file.")
                return
            
            if column2 not in df2.columns:
                st.error(f"Column '{column2}' not found in second file.")
                return

            # Perform comparison
            missing_codes, total_missing = compare_codes(df1, df2, column1, column2)

            # Display results
            st.subheader("Comparison Results")
            
            # Metrics
            col_metrics1, col_metrics2 = st.columns(2)
            with col_metrics1:
                st.metric(
                    label="Total Codes in First File", 
                    value=len(df1[column1].dropna())
                )
            with col_metrics2:
                st.metric(
                    label="Missing Codes", 
                    value=total_missing
                )

            # Detailed Results
            if missing_codes:
                st.markdown("### 🔍 Missing Codes")
                
                # Option to show full list or sample
                show_full = st.checkbox("Show Full List of Missing Codes")
                
                if show_full:
                    st.dataframe(pd.DataFrame(list(missing_codes), columns=['Missing Codes']))
                else:
                    st.dataframe(pd.DataFrame(list(missing_codes)[:50], columns=['Sample of Missing Codes']))
                
                # Download option
                missing_codes_df = pd.DataFrame(list(missing_codes), columns=['Missing Codes'])
                csv = missing_codes_df.to_csv(index=False)
                st.download_button(
                    label="Download Missing Codes",
                    data=csv,
                    file_name='missing_codes.csv',
                    mime='text/csv',
                )
            else:
                st.success("No missing codes found! 🎉")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Footer
    st.markdown("---")
    st.markdown("""
    ### About This Tool
    - Compare codes between two Excel files
    - Identify missing values across datasets
    - Easy to use, no coding required
    """)

if __name__ == "__main__":
    main()