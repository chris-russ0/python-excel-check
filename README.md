# Confronta Codici

Confronta Codici is a web application built with Flask that allows users to compare product codes from two Excel files. Users can upload their files, specify the columns to compare, and download the results.

## Features

- Upload two Excel files for comparison.
- Specify the columns to compare in each file.
- Download a text file with the results of the comparison.
- Sleek and modern user interface.

## Technologies Used

- Python
- Flask
- Pandas
- Bootstrap
- HTML/CSS

Usage
1. Upload the first Excel file and specify the column to compare.
2. Upload the second Excel file and specify the column to compare.
3. Click the "Confronta" button to perform the comparison.
4. View the total number of missing codes and download the result file.

## Project Structure
confronta-codici/
│
├── app.py
├── requirements.txt
├── static/
│   └── styles.css
└── templates/
    └── index.html


Certainly! Below is a sample README.md file for your Flask project. This file provides an overview of the project, setup instructions, and usage guidelines. You can copy and paste this into your GitHub repository.

Markdown

Collapse
# Confronta Codici

Confronta Codici is a web application built with Flask that allows users to compare product codes from two Excel files. Users can upload their files, specify the columns to compare, and download the results.

## Features

- Upload two Excel files for comparison.
- Specify the columns to compare in each file.
- Download a text file with the results of the comparison.
- Sleek and modern user interface.

## Technologies Used

- Python
- Flask
- Pandas
- Bootstrap
- HTML/CSS

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/confronta-codici.git
   cd confronta-codici
Create a Virtual Environment

BASH

python -m venv venv
Activate the Virtual Environment

On Windows:

BASH

venv\Scripts\activate
On macOS and Linux:

BASH

source venv/bin/activate
Install Dependencies

BASH

pip install -r requirements.txt
Run the Application

BASH

python app.py
Open the Application

Open your web browser and go to http://127.0.0.1:5000/.

## Usage
Upload the first Excel file and specify the column to compare.
Upload the second Excel file and specify the column to compare.
Click the "Confronta" button to perform the comparison.
View the total number of missing codes and download the result file.
Project Structure

confronta-codici/
│
├── app.py
├── requirements.txt
├── static/
│   └── styles.css
└── templates/
    └── index.html
## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes
