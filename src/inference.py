"""
Inference module for production deployment.
Loads trained models and makes predictions on new data.
"""

import numpy as np
import joblib
import os

try:
    from data_pipeline import clean_and_preprocess, prepare_feature_matrix
    from models import compute_decision_matrix
except ImportError:
    from .data_pipeline import clean_and_preprocess, prepare_feature_matrix
    from .models import compute_decision_matrix


class InsurancePredictor:
    """Loads trained models and makes predictions on new customer data."""

    def __init__(self, model_dir="models"):
        self.lapse_model, self.lapse_metadata = self._load_model_bundle(model_dir, "lapse_model")
        self.claim_model, self.claim_metadata = self._load_model_bundle(model_dir, "claim_model")

    @staticmethod
    def _load_model_bundle(model_dir, model_name):
        bundle_path = os.path.join(model_dir, f"{model_name}_bundle.pkl")
        if os.path.exists(bundle_path):
            bundle = joblib.load(bundle_path)
            return bundle["model"], bundle["metadata"]

        model_path = os.path.join(model_dir, f"{model_name}.pkl")
        if os.path.exists(model_path):
            raise FileNotFoundError(
                f"{bundle_path} is missing. Re-run src/train_pipeline.py so inference "
                "has the saved encoders, imputations, and feature list."
            )
        raise FileNotFoundError(f"Missing model artifact: {bundle_path}")

    def predict(self, df):
        """
        Predict lapse probability and claim cost for a DataFrame of customers.

        Parameters:
            df: DataFrame with required features (use preprocess method first)

        Returns:
            DataFrame with predictions and decision actions
        """
        df_processed = clean_and_preprocess(df)

        X_lapse, _ = prepare_feature_matrix(df_processed, metadata=self.lapse_metadata, fit=False)
        X_claim, _ = prepare_feature_matrix(df_processed, metadata=self.claim_metadata, fit=False)

        lapse_probs = self.lapse_model.predict_proba(X_lapse)[:, 1]
        claim_costs = np.expm1(self.claim_model.predict(X_claim))

        return compute_decision_matrix(df_processed, lapse_probs, claim_costs)
