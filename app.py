import os
import logging
from typing import Optional, Set, Union

import pandas as pd
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

class CodeComparisonApp:
    """
    A Flask-based web application for comparing codes across Excel files.
    """

    def __init__(self, app: Flask):
        """
        Initialize the application with configuration and logging.
        
        :param app: Flask application instance
        """
        self.app = app
        self.configure_logging()
        self.setup_routes()
        self.configure_upload_settings()

    def configure_logging(self):
        """
        Configure logging for the application.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def configure_upload_settings(self):
        """
        Configure file upload settings.
        """
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        self.app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
        
        # Ensure upload directory exists
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)

    def setup_routes(self):
        """
        Set up application routes.
        """
        self.app.add_url_rule('/', 'index', self.upload_files, methods=['GET', 'POST'])
        self.app.add_url_rule('/download', 'download', self.download_file)

    def allowed_file(self, filename: str) -> bool:
        """
        Check if the uploaded file has an allowed extension.
        
        :param filename: Name of the uploaded file
        :return: Boolean indicating if file is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.app.config['ALLOWED_EXTENSIONS']

    def compare_codes(
        self, 
        file1: FileStorage, 
        colonna1: str, 
        file2: FileStorage, 
        colonna2: str, 
        output_file: str = 'confronto_codici.txt'
    ) -> int:
        """
        Compare codes between two Excel files.
        
        :param file1: First uploaded file
        :param colonna1: Column name in first file
        :param file2: Second uploaded file
        :param colonna2: Column name in second file
        :param output_file: Path for output file
        :return: Number of missing codes
        """
        try:
            # Read Excel files
            df1 = pd.read_excel(file1)
            df2 = pd.read_excel(file2)

            # Validate column existence
            if colonna1 not in df1.columns or colonna2 not in df2.columns:
                raise ValueError(f"Columns {colonna1} or {colonna2} not found in files")

            # Extract and process codes
            codici1 = set(df1[colonna1].dropna())
            codici2 = set(df2[colonna2].dropna())

            # Find missing codes
            mancanti_in_file2 = codici1 - codici2

            # Write results to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"\n{'-'*40}\n")
                f.write(f"Codes in '{file1.filename}' missing from '{file2.filename}':\n")
                
                if mancanti_in_file2:
                    for codice in sorted(mancanti_in_file2):
                        # Convert float codes to integers if possible
                        if isinstance(codice, float) and codice.is_integer():
                            codice = int(codice)
                        f.write(f"{codice}\n")
                else:
                    f.write("No missing codes.\n")
                
                f.write(f"{'-'*40}\n")

            self.logger.info(f"Code comparison completed. Missing codes: {len(mancanti_in_file2)}")
            return len(mancanti_in_file2)

        except Exception as e:
            self.logger.error(f"Code comparison failed: {e}")
            raise

    def upload_files(self):
        """
        Handle file upload and code comparison.
        
        :return: Rendered template with results or error messages
        """
        if request.method == 'POST':
            # Validate file uploads
            if 'file1' not in request.files or 'file2' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file1 = request.files['file1']
            file2 = request.files['file2']

            # Check if files are selected
            if file1.filename == '' or file2.filename == '':
                flash('No selected file')
                return redirect(request.url)

            # Validate file types
            if not (self.allowed_file(file1.filename) and self.allowed_file(file2.filename)):
                flash('Invalid file type. Only Excel files are allowed.')
                return redirect(request.url)

            try:
                # Secure filenames
                filename1 = secure_filename(file1.filename)
                filename2 = secure_filename(file2.filename)

                # Save uploaded files
                filepath1 = os.path.join(self.app.config['UPLOAD_FOLDER'], filename1)
                filepath2 = os.path.join(self.app.config['UPLOAD_FOLDER'], filename2)
                file1.save(filepath1)
                file2.save(filepath2)

                # Get column names
                colonna1 = request.form['colonna1']
                colonna2 = request.form['colonna2']

                # Perform code comparison
                total_lines = self.compare_codes(
                    file1=filepath1, 
                    colonna1=colonna1, 
                    file2=filepath2, 
                    colonna2=colonna2
                )

                # Clean up uploaded files
                os.remove(filepath1)
                os.remove(filepath2)

                return render_template('index.html', total_lines=total_lines)

            except Exception as e:
                flash(f"An error occurred: {str(e)}")
                return redirect(request.url)

        return render_template('index.html')

    def download_file(self):
        """
        Provide download for comparison results.
        
        :return: Downloadable text file
        """
        try:
            return send_file('confronto_codici.txt', as_attachment=True)
        except FileNotFoundError:
            flash('No comparison results available.')
            return redirect(url_for('index'))

def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    :return: Configured Flask application
    """
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # For flash messages
    CodeComparisonApp(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)