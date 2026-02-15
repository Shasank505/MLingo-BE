import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.metrics import (
    accuracy_score, 
    r2_score, 
    f1_score, 
    mean_squared_error,
    precision_score,
    recall_score
)
from sklearn.model_selection import train_test_split
from typing import Dict, Any, Tuple
import os


class MLEvaluator:
    """Generic ML model evaluation engine"""
    
    def __init__(self, datasets_path: str = "./datasets"):
        self.datasets_path = datasets_path
        
    def load_dataset(self, dataset_name: str, config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """
        Load and split dataset into train/test sets
        
        Args:
            dataset_name: Name of the dataset file
            config: Configuration dict with target_column, test_size, etc.
            
        Returns:
            X_train, X_test, y_train, y_test
        """
        dataset_path = os.path.join(self.datasets_path, dataset_name)
        
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset {dataset_name} not found at {dataset_path}")
        
        # Load dataset
        df = pd.read_csv(dataset_path)
        
        # Extract target column
        target_column = config.get("target_column", df.columns[-1])
        
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Split data
        test_size = config.get("test_size", 0.2)
        random_state = config.get("random_state", 42)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        return X_train, X_test, y_train, y_test
    
    def load_model(self, model_path: str):
        """
        Load a trained ML model from file
        
        Supports: joblib (.pkl, .joblib), pickle (.pkl)
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        try:
            # Try joblib first
            model = joblib.load(model_path)
        except:
            # Fallback to pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        
        return model
    
    def evaluate_model(
        self, 
        model_path: str, 
        dataset_name: str, 
        metric_name: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate a trained model on a dataset
        
        Args:
            model_path: Path to the saved model
            dataset_name: Name of the dataset
            metric_name: Metric to evaluate ("accuracy", "r2_score", "f1_score")
            config: Dataset configuration
            
        Returns:
            Dict with score, passed status, and logs
        """
        try:
            # Load model
            model = self.load_model(model_path)
            
            # Load dataset
            X_train, X_test, y_train, y_test = self.load_dataset(dataset_name, config)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metric
            score = self._calculate_metric(y_test, y_pred, metric_name)
            
            # Additional metrics for logging
            additional_metrics = self._calculate_additional_metrics(y_test, y_pred, metric_name)
            
            logs = f"Metric: {metric_name}\nScore: {score:.4f}\n"
            logs += f"Additional metrics: {additional_metrics}"
            
            return {
                "score": float(score),
                "logs": logs,
                "success": True
            }
            
        except Exception as e:
            return {
                "score": 0.0,
                "logs": f"Evaluation failed: {str(e)}",
                "success": False
            }
    
    def _calculate_metric(self, y_true, y_pred, metric_name: str) -> float:
        """Calculate the specified metric"""
        metric_functions = {
            "accuracy": accuracy_score,
            "r2_score": r2_score,
            "f1_score": lambda y_t, y_p: f1_score(y_t, y_p, average='weighted'),
            "mse": mean_squared_error,
            "precision": lambda y_t, y_p: precision_score(y_t, y_p, average='weighted'),
            "recall": lambda y_t, y_p: recall_score(y_t, y_p, average='weighted'),
        }
        
        if metric_name not in metric_functions:
            raise ValueError(f"Unsupported metric: {metric_name}")
        
        return metric_functions[metric_name](y_true, y_pred)
    
    def _calculate_additional_metrics(self, y_true, y_pred, primary_metric: str) -> Dict[str, float]:
        """Calculate additional metrics for comprehensive evaluation"""
        metrics = {}
        
        try:
            # For classification tasks
            if primary_metric in ["accuracy", "f1_score", "precision", "recall"]:
                metrics["accuracy"] = accuracy_score(y_true, y_pred)
                metrics["f1_score"] = f1_score(y_true, y_pred, average='weighted')
                
            # For regression tasks
            elif primary_metric in ["r2_score", "mse"]:
                metrics["r2_score"] = r2_score(y_true, y_pred)
                metrics["mse"] = mean_squared_error(y_true, y_pred)
                metrics["rmse"] = np.sqrt(mean_squared_error(y_true, y_pred))
        except:
            pass
        
        return metrics
    
    def validate_model_format(self, model_path: str) -> bool:
        """Validate that the model file can be loaded"""
        try:
            self.load_model(model_path)
            return True
        except:
            return False