MANUALE UTENTE
Per prima cosa aprire il terminale e clonare il repository:
git clone  https://github.com/Michelez25/ICON25_26.git
Naviga all'interno della cartella principale:
cd ICON25_26
Prima di eseguire il progetto, è necessario installare le dipendenze richieste:
pip install -r requirements.txt
APRENDIMENTO SUPERVISIONATO
Spostandoti nella cartella dedicata mediante il comando:
cd ApprendimentoSupervisionato
Qui troviamo il dataset ed e' possibile eseguire i file  per eseguire le fasi di Preprocessing e Training and Evaluation.
Il comando da digitare è il seguente:
python nome_del_file.py
sostituendo nome_del_file.py con il file che si vuole eseguire 
Se si desidera visualizzare direttamente le valutazioni complessive dell'addestramento, esegui train_val_CHD.py. Per visualizzare i risultati di ogni fase e i grafici di distribuzione esegui separatamente i file: optimized_KNN_CHD.py, optimized_random_forest_CHD.py, optimized_decision_tree_CHD.py.
SISTEMA ESPERTO
Per eseguire il Sistema Esperto è necessario aver installato l'ambiente SWI-Prolog (assicurandosi di averlo aggiunto alla variabile di sistema PATH).Naviga all'interno della cartella del sistema esperto: cd SistemaEsperto
E digita il seguente comando per lanciare l'interfaccia utente:
python expert_system_CHD.py
Il sistema interrogherà la Knowledge Base (KB_CHD.pl) per fornire una diagnosi spiegabile calcolando un punteggio di rischio basato sui tratti clinici inseriti.
