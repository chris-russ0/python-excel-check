import pandas as pd

def confronta_codici(file1, colonna1, file2, colonna2, output_file):
    # Carica i file Excel
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Estrai le colonne dei codici prodotto, rimuovendo i valori NaN
    codici1 = set(df1[colonna1].dropna())
    codici2 = set(df2[colonna2].dropna())

    # Trova i codici mancanti in 'prodotti_anagrafica'
    mancanti_in_file2 = codici1 - codici2

    # Scrivi i risultati su un file di testo
    with open(output_file, 'w') as f:
        f.write(f"\n{'-'*40}\n")
        f.write(f"Codici presenti in '{file1}' ma mancanti in '{file2}':\n")
        if mancanti_in_file2:
            for codice in mancanti_in_file2:
                # Convert to integer if the number is a float with no fractional part
                if isinstance(codice, float) and codice.is_integer():
                    codice = int(codice)
                f.write(f"{codice}\n")
        else:
            f.write("Nessun codice mancante.\n")
        f.write(f"{'-'*40}\n")

    # Stampa il totale delle righe scritte
    print_total_lines(mancanti_in_file2)

def print_total_lines(missing_codes):
    total_lines = len(missing_codes)
    print(f"Total lines printed: {total_lines}")

# Specifica i nomi dei file e delle colonne
file1 = 'prodotti_online.xlsx'
colonna1 = 'Variant Barcode'
file2 = 'prodotti_anagrafica.xlsx'
colonna2 = 'UPC'
output_file = 'confronto_codici.txt'

# Esegui il confronto
confronta_codici(file1, colonna1, file2, colonna2, output_file)