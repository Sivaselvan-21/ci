import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

def run_rf_analysis(csv_file, split_ratio, tree_count):
    # 1. Load, Encode, and Split Data
    df = pd.read_csv(csv_file)
    for col in df.columns:
        df[col] = LabelEncoder().fit_transform(df[col])
    X, y = df.iloc[:, :-1], df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_ratio, random_state=42)

    # 2. Train Model and Predict
    model = RandomForestClassifier(n_estimators=tree_count, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # 3. Calculate and Print Metrics
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\n--- {int((1-split_ratio)*100)}-{int(split_ratio*100)} Split Results ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))
    print(f"Confusion Matrix:\n{cm}")
    print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

# Execute for 70/30 and 60/40 splits
run_rf_analysis('job_data.csv', 0.30, 100) 
run_rf_analysis('job_data.csv', 0.40, 100) 

