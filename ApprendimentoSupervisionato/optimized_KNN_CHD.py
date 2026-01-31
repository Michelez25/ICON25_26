from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import warnings


try:
    from preprocessing_CHD import df
except ImportError:
    print("ERRORE: Assicurati di aver salvato 'preprocessing_CHD.py' e 'dataset.csv' nella stessa directory.")
    exit()

warnings.simplefilter("ignore", category=FutureWarning)

print("\n----- Ricerca dei migliori iperparametri per KNN (su dati CHD) -----")

X = df.drop("chd", axis=1)
y = df["chd"]

n_runs = 10
n_neighbors = range(1, 31)

all_means = []  
all_stds = []   

for run in range(n_runs):
    print(f"Run {run + 1}/{n_runs}")
    
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=run, stratify=y)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    
    mean_scores = []
    std_scores = []

    # Calcolo della Cross-Validation per tutti i K
    for neighbors in n_neighbors:
        knn = KNeighborsClassifier(n_neighbors=neighbors)
        # Esegue la 5-fold cross-validation
        scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
        mean_scores.append(scores.mean())
        std_scores.append(scores.std())

    all_means.append(mean_scores)
    all_stds.append(std_scores)

# Calcola la media delle accuracy su tutte le 10 run per ogni n_neighbors
all_means_array = np.array(all_means)
mean_accuracy_for_neighbors = np.mean(all_means_array, axis=0)
# Calcola la deviazione standard delle accuracy su tutte le 10 run
std_accuracy_for_neighbors = np.std(all_means_array, axis=0)

# Trova il miglior K (n_neighbors) globale
best_global_neighbors = n_neighbors[np.argmax(mean_accuracy_for_neighbors)]

print(f"\nIl miglior n_neighbors globale è: {best_global_neighbors}")
print(f"Con un'Accuracy media (su 10 run) di: {mean_accuracy_for_neighbors[np.argmax(mean_accuracy_for_neighbors)]:.4f}")


# grafico finale accuracy media e std dei K
plt.figure(figsize=(10, 6), num = "KNN - CV Accuracy su 10 Run (CHD)")
plt.errorbar(
    n_neighbors, 
    mean_accuracy_for_neighbors, 
    yerr=std_accuracy_for_neighbors,
    fmt='o--', 
    capsize=4,
    elinewidth=2,
    markeredgewidth=2, 
    color = 'blue',
    label='Accuracy media ± std'
)
plt.axvline(
    x=best_global_neighbors, 
    color='red', 
    linestyle='--', 
    label=f'Miglior neighbors = {best_global_neighbors}'
)
plt.title("ACCURACY MEDIA E DEVIAZIONE STANDARD (SU 10 RUN) - KNN CHD", fontsize=14)
plt.xlabel("Valore di n_neighbors (K)")
plt.ylabel("Accuracy (Cross-Validation)")
plt.xticks(n_neighbors[::2]) 
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

run_summary = []
for i in range(n_runs):
    mean_run = np.mean(all_means_array[i])
    std_run = np.std(all_means_array[i])
    run_summary.append({'Run': i+1, 'CV Accuracy Media': mean_run, 'CV Std Media': std_run})

summary_df = pd.DataFrame(run_summary)

print("\nTabella riassuntiva delle run (Accuracy media di tutti i K):")
print(summary_df.to_string(index=False, float_format="%.4f"))