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
            
            # Validate file existence
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
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
            self.logger.error(f"Error processing {file_path}: {e}")
            raise

    def compare_codes(
        self, 
        file1: Union[str, Path], 
        column1: str, 
        file2: Union[str, Path], 
        column2: str, 
        output_file: Union[str, Path] = 'code_comparison.txt',
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
        :param output_file: Path for output file
        :param case_sensitive: Whether comparison is case-sensitive
        :param comparison_direction: Direction of comparison
        :param return_missing: Whether to return missing codes
        :return: Set of missing codes or None
        """
        try:
            # Convert to Path objects
            output_file = Path(output_file)
            
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
            
            # Write results to output file
            with output_file.open('w', encoding='utf-8') as f:
                f.write(f"\n{'-'*40}\n")
                f.write(f"{direction_msg}:\n")
                
                if missing_codes:
                    for code in sorted(missing_codes):
                        f.write(f"{code}\n")
                else:
                    f.write("No missing values.\n")
                
                f.write(f"{'-'*40}\n")
            
            # Log results
            self.logger.info(f"Comparison complete. Missing values: {len(missing_codes)}")
            self.logger.info(f"Results saved to: {output_file}")
            
            # Return missing codes if requested
            return missing_codes if return_missing else None
        
        except Exception as e:
            self.logger.error(f"Comparison failed: {e}")
            raise

def main():
    """
    Example usage of the CodeComparisonTool
    """
    try:
        # Initialize the comparison tool
        comparison_tool = CodeComparisonTool(log_level=logging.DEBUG)
        
        # Perform code comparison
        missing_codes = comparison_tool.compare_codes(
            file1='prodotti_online.xlsx',
            column1='Variant Barcode',
            file2='prodotti_anagrafica.xlsx',
            column2='UPC',
            output_file='code_comparison.txt',
            case_sensitive=False,
            comparison_direction='left_to_right',
            return_missing=True
        )
        
        # Optional: Additional processing of missing codes
        if missing_codes:
            print(f"Missing codes: {missing_codes}")
    
    except Exception as e:
        logging.error(f"Execution failed: {e}")

if __name__ == "__main__":
    main()