from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

def confronta_codici(file1, colonna1, file2, colonna2, output_file):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    codici1 = set(df1[colonna1].dropna())
    codici2 = set(df2[colonna2].dropna())

    mancanti_in_file2 = codici1 - codici2

    with open(output_file, 'w') as f:
        f.write(f"\n{'-'*40}\n")
        f.write(f"Codici presenti in '{file1}' ma mancanti in '{file2}':\n")
        if mancanti_in_file2:
            for codice in mancanti_in_file2:
                if isinstance(codice, float) and codice.is_integer():
                    codice = int(codice)
                f.write(f"{codice}\n")
        else:
            f.write("Nessun codice mancante.\n")
        f.write(f"{'-'*40}\n")

    return len(mancanti_in_file2)

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        colonna1 = request.form['colonna1']
        colonna2 = request.form['colonna2']
        output_file = 'confronto_codici.txt'

        file1.save(file1.filename)
        file2.save(file2.filename)

        total_lines = confronta_codici(file1.filename, colonna1, file2.filename, colonna2, output_file)

        os.remove(file1.filename)
        os.remove(file2.filename)

        return render_template('index.html', total_lines=total_lines, output_file=output_file)

    return render_template('index.html')

@app.route('/download')
def download_file():
    return send_file('confronto_codici.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)