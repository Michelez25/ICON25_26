:- dynamic ha_tratto/3.

% Pesi per i tratti di rischio cardiovascolare (semplificati e illustrativi)
% peso(TipoRischio, Tratto, Valore, Punteggio)
% Un punteggio totale maggiore indica un rischio più alto.

% --- 1. Storia Familiare (famhist) ---
% presente -> rischio alto
peso(alto_rischio, famhist, presente, 5).
peso(basso_rischio, famhist, assente, 1).

% --- 2. Consumo di Tabacco (tabacco) ---
% Alto (es. > 500 g/anno)
peso(alto_rischio, tobacco, alto, 5).
% Medio (es. 1 - 500 g/anno)
peso(medio_rischio, tobacco, medio, 3).
% Basso (0)
peso(basso_rischio, tobacco, basso, 1).

% --- 3. Età (age) ---
% Anziano (es. > 55 anni)
peso(alto_rischio, age, anziano, 4).
% Adulto (es. 40 - 55 anni)
peso(medio_rischio, age, adulto, 2).
% Giovane (es. < 40 anni)
peso(basso_rischio, age, giovane, 1).

% --- 4. Pressione Sistolica (sbp) ---
% Alta (es. > 140 mmHg)
peso(alto_rischio, sbp, alta, 4).
% Normale (es. 120 - 140 mmHg)
peso(medio_rischio, sbp, normale, 2).
% Ottimale (es. < 120 mmHg)
peso(basso_rischio, sbp, ottimale, 1).

% --- 5. Colesterolo LDL (ldl) ---
% Alto (es. > 400 mg/dl)
peso(alto_rischio, ldl, alto, 3).
% Normale
peso(basso_rischio, ldl, normale, 1).


% --- Calcolo del Punteggio Totale ---
% Trova tutti i pesi associati ai tratti della Persona per un dato TipoRischio e li somma.
calcola_punteggio(Persona, TipoRischio, Totale) :-
    findall(Peso, (ha_tratto(Persona, Tratto, Valore), peso(TipoRischio, Tratto, Valore, Peso)), ListaPesi),
    sum_list(ListaPesi, Totale).

% --- Classificazione Finale ---
% classificazione(Persona, LivelloRischio, PunteggioAlto, PunteggioBasso)
classificazione(Persona, LivelloRischio, PunteggioAlto, PunteggioBasso) :-
    % Calcolo del punteggio totale per rischio alto e basso
    calcola_punteggio(Persona, alto_rischio, PunteggioAlto),
    calcola_punteggio(Persona, basso_rischio, PunteggioBasso),
    
    % Regole di decisione (simili alla logica a punteggio del tuo PDF):
    % Le soglie (10 e 5) sono state scelte in modo arbitrario per fini dimostrativi.
    (PunteggioAlto >= 10, LivelloRischio = 'RISCHIO ALTO (Consultare medico)';
     PunteggioAlto >= 5, LivelloRischio = 'RISCHIO MEDIO (Monitoraggio)';
     LivelloRischio = 'RISCHIO BASSO (Buono stato)').