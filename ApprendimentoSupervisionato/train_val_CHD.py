from preprocessing_CHD import df
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Preparazione Dati
X = df.drop("chd", axis=1)
y = df["chd"]

# Split dei dati (80% training, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

# Standardizzazione
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Definizione Modelli con parametri ottimizzati
models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=100, 
        max_depth=10, 
        class_weight='balanced', 
        random_state=42
    ),
    'Decision Tree': DecisionTreeClassifier(
        max_depth=5, 
        class_weight='balanced', 
        random_state=42
    ),
    'KNN': KNeighborsClassifier(
        n_neighbors=15, 
        weights='distance'
    )
}

accuracy_results = []

# 4. Addestramento e Stampa
if __name__ == "__main__":
    for name, model in models.items():
        # Addestramento
        model.fit(X_train_scaled, y_train)
        
        # Predizione e calcolo accuracy
        y_preds = model.predict(X_test_scaled)
        acc = accuracy_score(y_test, y_preds)

        print(f"\n{'-'*10} {name} {'-'*10}")
        print(f"Accuracy: {acc:.3f}")
        print("Classification Report:\n", 
              classification_report(y_test, y_preds, target_names=['No CHD', 'CHD']))

        accuracy_results.append({'Modello': name, 'Accuracy': acc})
    
    # Tabella riassuntiva finale
    results_df = pd.DataFrame(accuracy_results).sort_values(by='Accuracy', ascending=False)
    print("\n----- Riassunto Accuracy Modelli -----")
    print(results_df.to_string(index=False, float_format="%.3f"))