import streamlit as st
import pandas as pd
import logging
from typing import Optional, Set, Union
from pathlib import Path

class CodeComparisonTool:
    """
    A comprehensive tool for comparing codes across Excel files with advanced features.
    """
    
    def __init__(
        self, 
        log_level: int = logging.INFO,
        log_format: str = '%(asctime)s - %(levelname)s: %(message)s'
    ):
        """
        Initialize the comparison tool with logging configuration.
        
        :param log_level: Logging level (default: logging.INFO)
        :param log_format: Format for log messages
        """
        # Configure logging
        logging.basicConfig(level=log_level, format=log_format)
        self.logger = logging.getLogger(__name__)

    def _load_excel_column(
        self, 
        file_path: Union[str, Path], 
        column_name: str, 
        case_sensitive: bool = False
    ) -> Set[str]:
        """
        Load and process a specific column from an Excel file.
        
        :param file_path: Path to the Excel file
        :param column_name: Name of the column to extract
        :param case_sensitive: Whether comparison should be case-sensitive
        :return: Set of processed column values
        """
        try:
            # Convert to Path object for better handling
            file_path = Path(file_path)
            
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate column existence
            if column_name not in df.columns:
                raise ValueError(f"Column '{column_name}' not found in {file_path}")
            
            # Process column values
            if case_sensitive:
                return set(df[column_name].dropna().astype(str))
            else:
                return set(df[column_name].dropna().astype(str).str.lower())
        
        except Exception as e:
            st.error(f"Error processing {file_path}: {e}")
            raise

    def compare_codes(
        self, 
        file1: Union[str, Path], 
        column1: str, 
        file2: Union[str, Path], 
        column2: str, 
        case_sensitive: bool = False,
        comparison_direction: str = 'left_to_right',
        return_missing: bool = False
    ) -> Optional[Set[str]]:
        """
        Compare codes between two Excel files.
        
        :param file1: First Excel file path
        :param column1: Column name in first file
        :param file2: Second Excel file path
        :param column2: Column name in second file
        :param case_sensitive: Whether comparison is case-sensitive
        :param comparison_direction: Direction of comparison
        :param return_missing: Whether to return missing codes
        :return: Set of missing codes or None
        """
        try:
            # Load codes from both files
            codes1 = self._load_excel_column(file1, column1, case_sensitive)
            codes2 = self._load_excel_column(file2, column2, case_sensitive)
            
            # Determine comparison direction
            if comparison_direction == 'left_to_right':
                missing_codes = codes1 - codes2
                direction_msg = f"Values in '{file1}' missing from '{file2}'"
            elif comparison_direction == 'right_to_left':
                missing_codes = codes2 - codes1
                direction_msg = f"Values in '{file2}' missing from '{file1}'"
            else:
                raise ValueError("Invalid comparison direction")
            
            # Log results
            st.info(f"Comparison complete. Missing values: {len(missing_codes)}")
            
            # Return missing codes if requested
            return missing_codes if return_missing else None
        
        except Exception as e:
            st.error(f"Comparison failed: {e}")
            raise

def main():
    """
    Streamlit app for Code Comparison Tool
    """
    # Page configuration
    st.set_page_config(
        page_title="Code Comparison Tool",
        page_icon="🔍",
        layout="wide"
    )

    # Title and description
    st.title("📊 Excel Code Comparison Tool")
    st.markdown("Compare codes between two Excel files and identify missing values.")

    # Initialize the comparison tool
    comparison_tool = CodeComparisonTool(log_level=logging.INFO)

    # Sidebar for configuration
    st.sidebar.header("📝 Comparison Settings")

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

    # Comparison options
    col_sensitive, col_direction = st.columns(2)
    
    with col_sensitive:
        case_sensitive = st.checkbox("Case Sensitive Comparison", value=False)
    
    with col_direction:
        comparison_direction = st.selectbox(
            "Comparison Direction",
            ["Left to Right", "Right to Left"],
            index=0
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
            # Perform comparison
            missing_codes = comparison_tool.compare_codes(
                file1=file1,
                column1=column1,
                file2=file2,
                column2=column2,
                case_sensitive=case_sensitive,
                comparison_direction=comparison_direction.lower().replace(" ", "_"),
                return_missing=True
            )

            # Display results
            st.subheader("Comparison Results")
            
            if missing_codes:
                # Metrics
                st.metric(label="Missing Codes", value=len(missing_codes))
                
                # Show missing codes
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
    - Flexible comparison options
    """)

if __name__ == "__main__":
    main()