import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from preprocessing_CHD import df

X = df.drop("chd", axis=1)
y = df["chd"]

# Definiamo la Pipeline: prima scala i dati, poi applica il classificatore
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

param_grid = {'knn__n_neighbors': range(1, 31)}

outer_cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

means_cv = []
stds_cv = []

print("\n--- Esecuzione Nested CV: KNN con Scaling (Generazione Risultati) ---")

for i, (train_idx, test_idx) in enumerate(outer_cv.split(X, y)):
    X_train_outer, y_train_outer = X.iloc[train_idx], y.iloc[train_idx]
    
    # Loop Interno: GridSearchCV sulla pipeline
    grid_search = GridSearchCV(pipe, param_grid=param_grid, cv=inner_cv, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train_outer, y_train_outer)
    
    means_cv.append(grid_search.best_score_)
    stds_cv.append(grid_search.cv_results_['std_test_score'][grid_search.best_index_])
    print(f"Completata Run {i+1}/10")

summary_df = pd.DataFrame({'Run': range(1, 11), 'CV Accuracy': means_cv, 'CV Std': stds_cv})
print("\nTabella riassuntiva delle run (KNN):")
print(summary_df.to_string(index=False, float_format="%.4f"))

plt.figure(figsize=(10, 6))
plt.errorbar(summary_df['Run'], summary_df['CV Accuracy'], yerr=summary_df['CV Std'], fmt='o--', color='blue', capsize=4)
plt.title("ACCURACY MEDIA E DEVIAZIONE STANDARD (SU 10 RUN) - KNN CHD", fontsize=14)
plt.xlabel("Numero di Run (Outer Fold)")
plt.ylabel("Accuracy (Cross-Validation)")
plt.grid(True)
plt.xticks(range(1, 11))
plt.tight_layout()
plt.show()