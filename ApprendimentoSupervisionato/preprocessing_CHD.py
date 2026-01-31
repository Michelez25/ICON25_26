import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(current_dir, "dataset.csv") 

try:
    df = pd.read_csv(file_name, sep=';')
    
    if df.shape[1] <= 1:
        df = pd.read_csv(file_name, sep=',')
        
    print(f"File caricato con successo! Colonne trovate: {df.columns.tolist()}")
except Exception as e:
    print(f"ERRORE: Non trovo il file in {file_name}. Dettaglio: {e}")
    df = pd.DataFrame()
    
if not df.empty:
    # 1. Rimozione della colonna 'ind' (indice)
    if 'ind' in df.columns:
        df.drop('ind', axis=1, inplace=True)

    # 2. Conversione della variabile categorica 'famhist': 'Present' -> 1, 'Absent' -> 0
    famhist_map = {'Present': 1, 'Absent': 0}
    df['famhist'] = df['famhist'].map(famhist_map)
    
    print("\n----- Prime righe del dataset cardiovascolare pre-elaborato -----")
    print(df.head())

    if __name__ == "__main__":
        print("\n----- Informazioni sul dataset dopo il preprocessing -----")
        print(df.info())