import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from scipy.stats import randint
from preprocessing_CHD import df

# Preparazione dati
X = df.drop("chd", axis=1)
y = df["chd"]

# Definizione iperparametri da testare
param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Struttura Nested CV: 10 fold esterni (le "Run") e 5 fold interni (il Tuning)
outer_cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

means_cv = []
stds_cv = []

print("\n--- Esecuzione Nested CV: Random Forest (Generazione Risultati) ---")

for i, (train_idx, test_idx) in enumerate(outer_cv.split(X, y)):
    X_train_outer, y_train_outer = X.iloc[train_idx], y.iloc[train_idx]
    
    rf = RandomForestClassifier(random_state=42)
    # Loop Interno: Ricerca dei parametri migliori sul training set dell'outer fold
    random_search = RandomizedSearchCV(
        rf, param_distributions=param_dist, n_iter=15, cv=inner_cv, 
        scoring='accuracy', n_jobs=-1, random_state=42
    )
    random_search.fit(X_train_outer, y_train_outer)
    
    # Salvataggio metriche per la tabella
    means_cv.append(random_search.best_score_)
    stds_cv.append(random_search.cv_results_['std_test_score'][random_search.best_index_])
    print(f"Completata Run {i+1}/10")

# Tabella riassuntiva
summary_df = pd.DataFrame({'Run': range(1, 11), 'CV Accuracy': means_cv, 'CV Std': stds_cv})
print("\nTabella riassuntiva delle run (Random Forest):")
print(summary_df.to_string(index=False, float_format="%.4f"))

# Grafico
plt.figure(figsize=(10, 6))
plt.errorbar(summary_df['Run'], summary_df['CV Accuracy'], yerr=summary_df['CV Std'], fmt='o', capsize=5, elinewidth=2)
plt.title("ACCURACY MEDIA E DEVIAZIONE STANDARD (SU 10 RUN) - RANDOM FOREST CHD", fontsize=14)
plt.xlabel("Numero di Run")
plt.ylabel("Accuracy")
plt.grid(True)
plt.xticks(range(1, 11))
plt.tight_layout()
plt.show()