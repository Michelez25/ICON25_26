from pyswip import Prolog
import warnings


warnings.simplefilter("ignore", category=FutureWarning)

#Funzioni di input 

def ask_yes_no(question):
    """Chiede una risposta 'si' o 'no' e la restituisce in formato Prolog."""
    while True:
        risposta = input(f"{question} (si/no): ").lower()
        if risposta in ['si', 'no']:
            return 'presente' if risposta == 'si' else 'assente'
        print("ERRORE: Inserimento non valido, per favore inserisci 'si' o 'no'.")

def ask_numeric(question):
    """Chiede un numero intero."""
    while True:
        risposta_str = input(f"{question} ").strip()
        try:
            numero = int(risposta_str)
            return numero
        except ValueError:
            print("ERRORE: Inserimento non valido, per favore inserisci un numero intero.")


#Funzione per l'Analisi CHD
def run_chd_expert_system():
    prolog = Prolog()
    try:
        # Carica la Base di Conoscenza CHD
        prolog.consult("KB_CHD.pl")
    except Exception as e:
        print(f"ERRORE: Impossibile caricare 'KB_CHD.pl'. Assicurati che il file sia nella stessa cartella e che Prolog sia configurato.")
        print(f"Dettaglio errore: {e}")
        return

    print("\n--- Sistema Esperto per la Predizione del Rischio Cardiovascolare (CHD) ---")
    
    # Storia Familiare (famhist)
    risposta_famhist = ask_yes_no("\nC'e' una storia familiare di malattia cardiaca precoce?")
    prolog.assertz(f"ha_tratto(utente, famhist, {risposta_famhist})")

    # Età (age)
    age = ask_numeric("\nQual è l'età del paziente? (in anni)")
    if age > 55:
        categoria_age = 'anziano'
    elif age >= 40:
        categoria_age = 'adulto'
    else:
        categoria_age = 'giovane'
    prolog.assertz(f"ha_tratto(utente, age, {categoria_age})")

    # Pressione Sistolica (sbp)
    sbp = ask_numeric("\nQual è la pressione sanguigna sistolica (il valore più alto)? (in mmHg)")
    if sbp > 140:
        categoria_sbp = 'alta'
    elif sbp >= 120:
        categoria_sbp = 'normale'
    else:
        categoria_sbp = 'ottimale'
    prolog.assertz(f"ha_tratto(utente, sbp, {categoria_sbp})")
    
    # Consumo di Tabacco (tobacco)
    tobacco = ask_numeric("\nQual è il consumo cumulativo di tabacco? (stimato in grammi/anno)")
    if tobacco > 500:
        categoria_tobacco = 'alto'
    elif tobacco > 0:
        categoria_tobacco = 'medio'
    else:
        categoria_tobacco = 'basso'
    prolog.assertz(f"ha_tratto(utente, tobacco, {categoria_tobacco})")
    
    # Colesterolo (ldl)
    ldl = ask_numeric("\nQual è il livello di colesterolo LDL? (in mg/dl)")
    categoria_ldl = 'alto' if ldl > 400 else 'normale'
    prolog.assertz(f"ha_tratto(utente, ldl, {categoria_ldl})")

    # Interrogazione della KB per determinare il rischio
    print("\n--- Analisi del rischio in corso... ---")
    try:
        
        query = list(prolog.query("classificazione(utente, LivelloRischio, P1, P2)")) 

        if query:
            res = query[0]
            livello = res["LivelloRischio"]
            p1 = res["P1"] 
            
            SOGLIA_ALTO_RISCHIO = 10 
            
            print("\n=======================================================")
            print(f"RISULTATO: {str(livello).upper()}")
            print("\n  Punteggio accumulato a favore del rischio: *{:.2f}* punti".format(p1))
            print(f"  Soglia minima per la classificazione 'Rischio Alto': *{SOGLIA_ALTO_RISCHIO:.2f}* punti")
            print("=======================================================")

            if p1 >= SOGLIA_ALTO_RISCHIO:
                 print("\nCONFERMA: Il tuo punteggio ({:.2f}) ha superato o eguagliato la soglia critica, indicando la necessità di attenzione medica.".format(p1))
            elif p1 >= 5 and p1 < SOGLIA_ALTO_RISCHIO:
                print("\nCONFERMA: Il punteggio ({:.2f}) indica un rischio MEDIO, ma non ha superato la soglia di Rischio ALTO.".format(p1))
            else:
                print("\nCONFERMA: Il punteggio ({:.2f}) è al di sotto della soglia, indicando un rischio BASSO.".format(p1))
                
        else:
            print("Nessun risultato di classificazione trovato.")
            
    except Exception as e:
        print(f"\nERRORE durante l'interrogazione della KB: {e}")

if __name__ == "__main__":
    run_chd_expert_system()