import pandas as pd
from pyswip import Prolog

prolog = Prolog()
prolog.consult("KB_CHD.pl")

def carica_fatti(dati):
    prolog.retractall("ha_tratto(_, _, _)")
    for k, v in dati.items():
        prolog.assertz(f"ha_tratto('utente', {k}, {v})")

def main():
    print("="*40)
    print(" SISTEMA ESPERTO CARDIOVASCOLARE")
    print("="*40)
    print("Inserisci i parametri richiesti per l'analisi:")

    try:
        sbp = int(input("> Pressione Sistolica (mmHg): "))
        ldl = float(input("> Livello Colesterolo LDL: "))
        tobacco = float(input("> Consumo cumulativo di tabacco (kg): "))
        fam = input("> Ha familiari con patologie cardiache? (s/n): ").lower()
        age = int(input("> Età del paziente: "))

        dati = {
            'sbp': sbp, 'ldl': ldl, 'tobacco': tobacco,
            'famhist': 1 if fam == 's' else 0, 'age': age
        }
        carica_fatti(dati)

        risultato = list(prolog.query("rischio_cardiovascolare('utente', L)"))
        livello = risultato[0]['L'] if risultato else "NON_CLASSIFICABILE"

        motivi = list(prolog.query("spiega_diagnosi('utente', M)"))
        
        print("\n" + "="*40)
        print(f"ESITO ANALISI: RISCHIO {livello}")
        print("-"*40)
        
        if motivi:
            print("MOTIVAZIONI CLINICHE RILEVATE:")
            for m in motivi:
                print(f" - {m['M']}")
        else:
            print("Nessun fattore di rischio critico rilevato.")
        
    except ValueError:
        print("\nERRORE: Inserire valori numerici validi.")

if __name__ == "__main__":
    main()