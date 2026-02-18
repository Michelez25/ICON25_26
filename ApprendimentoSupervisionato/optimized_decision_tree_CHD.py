import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from preprocessing_CHD import df

X = df.drop("chd", axis=1)
y = df["chd"]

param_dist = {
    'max_depth': [None, 3, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10, 15],
    'min_samples_leaf': [1, 2, 4, 6]
}

# Definiamo la struttura Nested CV (10 fold esterni)
outer_cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

means_cv = []
stds_cv = []

print("\n--- Esecuzione Nested CV: Generazione risultati per tabella ---")

# Ciclo esplicito sui 10 fold (le tue "Run")
for i, (train_idx, test_idx) in enumerate(outer_cv.split(X, y)):
    X_train_outer = X.iloc[train_idx]
    y_train_outer = y.iloc[train_idx]

    dt = DecisionTreeClassifier(random_state=42)
    # Ricerca iperparametri sul set di training dell'outer fold
    random_search = RandomizedSearchCV(dt, param_distributions=param_dist, n_iter=15, cv=inner_cv, scoring='accuracy', n_jobs=-1, random_state=42)
    random_search.fit(X_train_outer, y_train_outer)

    # Estraiamo i dati per la tua tabella
    means_cv.append(random_search.best_score_)
    stds_cv.append(random_search.cv_results_['std_test_score'][random_search.best_index_])
    print(f"Completata Run {i+1}/10")

# Creazione Tabella
summary_df = pd.DataFrame({'Run': range(1, 11), 'CV Accuracy': means_cv, 'CV Std': stds_cv})
print("\nTabella riassuntiva delle run (Decision Tree):")
print(summary_df.to_string(index=False, float_format="%.4f"))

# Creazione Grafico (uguale all'originale)
plt.figure(figsize=(10, 6))
plt.errorbar(summary_df['Run'], summary_df['CV Accuracy'], yerr=summary_df['CV Std'], fmt='o', capsize=5)
plt.title("ACCURACY MEDIA E DEVIAZIONE STANDARD (SU 10 RUN) - DECISION TREE CHD")
plt.xlabel("Numero di Run")
plt.ylabel("Accuracy")
plt.grid(True)
plt.xticks(range(1, 11))
plt.show()