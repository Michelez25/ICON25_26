% La diagnosi viene risolta in ordine di priorità clinica
% Il sistema prova a dimostrare il rischio ALTO prima di passare agli altri

rischio_cardiovascolare(P, 'ALTO') :- profilo_emergenza(P).
rischio_cardiovascolare(P, 'ALTO') :- sindrome_metabolica(P).
rischio_cardiovascolare(P, 'MEDIO') :- iperteso(P).
rischio_cardiovascolare(P, 'MEDIO') :- forte_fumatore(P).
rischio_cardiovascolare(_, 'BASSO').

% Queste regole catturano i casi limite dove un singolo valore è patologico.

profilo_emergenza(P) :- ipercolesterolemia_estrema(P).
profilo_emergenza(P) :- crisi_ipertensiva(P).


% Implementa il ragionamento clinico su combinazioni di fattori.

sindrome_metabolica(P) :- 
    iperteso(P), 
    ipercolesterolemia(P), 
    (forte_fumatore(P) ; soggetto_anziano(P)).


% Trasformano i fatti numerici in simboli logici.

ipercolesterolemia_estrema(P) :- 
    ha_tratto(P, ldl, V), V >= 250.

crisi_ipertensiva(P) :- 
    ha_tratto(P, sbp, V), V >= 180.

iperteso(P) :- 
    ha_tratto(P, sbp, V), V >= 140.

ipercolesterolemia(P) :- 
    ha_tratto(P, ldl, V), V >= 160.

forte_fumatore(P) :- 
    ha_tratto(P, tobacco, V), V >= 15.

soggetto_anziano(P) :- 
    ha_tratto(P, age, V), V >= 65.


% Permette al sistema di spiegare il risultato all'utente

spiega_diagnosi(P, 'Emergenza: Livelli di LDL estremamente alti (>250)') :- ipercolesterolemia_estrema(P).
spiega_diagnosi(P, 'Emergenza: Pressione sistolica in fase critica (>180)') :- crisi_ipertensiva(P).
spiega_diagnosi(P, 'Condizione di Ipertensione rilevata') :- iperteso(P).
spiega_diagnosi(P, 'Livelli di colesterolo LDL superiori alla norma') :- ipercolesterolemia(P).
spiega_diagnosi(P, 'Stato di forte tabagismo attivo') :- forte_fumatore(P).
spiega_diagnosi(P, 'Paziente in età avanzata (fattore di rischio naturale)') :- soggetto_anziano(P).
spiega_diagnosi(P, 'Quadro clinico compatibile con Sindrome Metabolica') :- sindrome_metabolica(P).