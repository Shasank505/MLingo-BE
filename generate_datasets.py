"""
Generate sample datasets for ML quests
"""
import pandas as pd
import numpy as np
from sklearn.datasets import make_regression, make_classification, load_iris
import os

def create_housing_dataset():
    """Create synthetic housing price dataset"""
    np.random.seed(42)
    
    # Generate base features
    n_samples = 1000
    
    X, y = make_regression(
        n_samples=n_samples,
        n_features=8,
        n_informative=6,
        noise=10,
        random_state=42
    )
    
    # Create meaningful feature names
    df = pd.DataFrame(X, columns=[
        'square_feet', 'bedrooms', 'bathrooms', 'age',
        'garage_size', 'lot_size', 'proximity_to_city', 'school_rating'
    ])
    
    # Scale target to realistic house prices
    y = (y - y.min()) / (y.max() - y.min()) * 400000 + 100000
    df['price'] = y
    
    # Add some non-linear relationships
    df['price'] = df['price'] + df['square_feet'] * 50 + df['bedrooms'] * 10000
    
    return df


def create_churn_dataset():
    """Create synthetic customer churn dataset"""
    np.random.seed(42)
    
    n_samples = 2000
    
    X, y = make_classification(
        n_samples=n_samples,
        n_features=10,
        n_informative=7,
        n_redundant=2,
        n_classes=2,
        weights=[0.7, 0.3],
        random_state=42
    )
    
    df = pd.DataFrame(X, columns=[
        'tenure', 'monthly_charges', 'total_charges', 'contract_length',
        'payment_method', 'internet_service', 'tech_support', 'streaming_tv',
        'online_security', 'paperless_billing'
    ])
    
    df['churn'] = y
    
    return df


def create_iris_dataset():
    """Create iris classification dataset"""
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = iris.target
    
    return df


def generate_all_datasets(output_dir='./datasets'):
    """Generate all sample datasets"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Housing dataset
    housing_df = create_housing_dataset()
    housing_df.to_csv(os.path.join(output_dir, 'housing_train.csv'), index=False)
    print(f"✅ Created housing_train.csv ({len(housing_df)} samples)")
    
    # Churn dataset
    churn_df = create_churn_dataset()
    churn_df.to_csv(os.path.join(output_dir, 'churn_train.csv'), index=False)
    print(f"✅ Created churn_train.csv ({len(churn_df)} samples)")
    
    # Iris dataset
    iris_df = create_iris_dataset()
    iris_df.to_csv(os.path.join(output_dir, 'iris_train.csv'), index=False)
    print(f"✅ Created iris_train.csv ({len(iris_df)} samples)")


if __name__ == "__main__":
    print("Generating sample datasets...")
    generate_all_datasets()
    print("\n✅ All datasets generated successfully!")