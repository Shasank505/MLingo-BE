"""
Train sample ML models for testing quest submissions
"""
import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, f1_score


def train_housing_model():
    """Train a model for housing price prediction"""
    df = pd.read_csv('./datasets/housing_train.csv')
    
    X = df.drop(columns=['price'])
    y = df['price']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train simple linear regression (should pass Quest 1)
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    y_pred = model_lr.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    
    joblib.dump(model_lr, './sample_models/housing_linear_regression.pkl')
    print(f"✅ Linear Regression - R² Score: {r2:.4f}")
    
    # Train random forest (should pass Quest 2)
    model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_rf.fit(X_train, y_train)
    y_pred_rf = model_rf.predict(X_test)
    r2_rf = r2_score(y_test, y_pred_rf)
    
    joblib.dump(model_rf, './sample_models/housing_random_forest.pkl')
    print(f"✅ Random Forest - R² Score: {r2_rf:.4f}")


def train_churn_model():
    """Train a model for customer churn prediction"""
    df = pd.read_csv('./datasets/churn_train.csv')
    
    X = df.drop(columns=['churn'])
    y = df['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train logistic regression
    model_lr = LogisticRegression(max_iter=1000, random_state=42)
    model_lr.fit(X_train, y_train)
    y_pred = model_lr.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    joblib.dump(model_lr, './sample_models/churn_logistic_regression.pkl')
    print(f"✅ Logistic Regression - Accuracy: {acc:.4f}")
    
    # Train random forest
    model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    model_rf.fit(X_train, y_train)
    y_pred_rf = model_rf.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    
    joblib.dump(model_rf, './sample_models/churn_random_forest.pkl')
    print(f"✅ Random Forest - Accuracy: {acc_rf:.4f}")


def train_iris_model():
    """Train a model for iris classification"""
    df = pd.read_csv('./datasets/iris_train.csv')
    
    X = df.drop(columns=['species'])
    y = df['species']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train random forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    joblib.dump(model, './sample_models/iris_random_forest.pkl')
    print(f"✅ Iris RF - Accuracy: {acc:.4f}, F1-Score: {f1:.4f}")


def main():
    """Train all sample models"""
    os.makedirs('./sample_models', exist_ok=True)
    
    print("Training housing models...")
    train_housing_model()
    
    print("\nTraining churn models...")
    train_churn_model()
    
    print("\nTraining iris models...")
    train_iris_model()
    
    print("\n✅ All sample models trained successfully!")


if __name__ == "__main__":
    main()