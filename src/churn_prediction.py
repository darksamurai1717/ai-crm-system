import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os
from datetime import datetime, timedelta


class ChurnPredictor:
    def __init__(self, model_path='models/churn_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False

    def generate_customer_data(self, leads_df):
        """Generate synthetic customer data for churn prediction"""
        # Filter converted leads as customers
        customers = leads_df[leads_df['status'] == 'Converted'].copy()

        if len(customers) == 0:
            # Create some sample customers
            sample_customers = pd.DataFrame({
                'customer_id': range(1, 11),
                'name': [f'Customer {i}' for i in range(1, 11)],
                'email': [f'customer{i}@example.com' for i in range(1, 11)],
                'signup_date': [datetime.now() - timedelta(days=np.random.randint(30, 365)) for _ in range(10)],
                'last_login': [datetime.now() - timedelta(days=np.random.randint(0, 60)) for _ in range(10)]
            })
            customers = sample_customers

        # Add synthetic features for existing customers
        np.random.seed(42)

        # Fix the datetime calculation - CORRECTED VERSION
        if 'signup_date' in customers.columns:
            # Convert signup_date to datetime if it's not already
            customers['signup_date'] = pd.to_datetime(customers['signup_date'])
            # Calculate days since signup correctly
            customers['days_since_signup'] = (datetime.now() - customers['signup_date']).dt.days
        else:
            # If no signup_date, create random values
            customers['days_since_signup'] = np.random.randint(30, 365, len(customers))

        # Add other synthetic features
        customers['days_since_last_login'] = np.random.randint(0, 60, len(customers))
        customers['monthly_spend'] = np.random.normal(100, 50, len(customers))
        customers['support_tickets'] = np.random.poisson(2, len(customers))
        customers['feature_usage_score'] = np.random.uniform(0, 100, len(customers))

        # Create churn labels (synthetic for demo)
        churn_probability = (
                (customers['days_since_last_login'] > 30).astype(int) * 0.4 +
                (customers['support_tickets'] > 3).astype(int) * 0.3 +
                (customers['feature_usage_score'] < 30).astype(int) * 0.3
        )
        customers['will_churn'] = (churn_probability > 0.5).astype(int)

        return customers

    def prepare_features(self, customers_df):
        """Prepare features for churn prediction"""
        features = customers_df[[
            'days_since_signup', 'days_since_last_login',
            'monthly_spend', 'support_tickets', 'feature_usage_score'
        ]].copy()

        # Handle missing values
        features = features.fillna(features.mean())

        return features

    def train_model(self, customers_df):
        """Train churn prediction model"""
        try:
            if len(customers_df) < 5:
                print("Not enough customer data to train model.")
                return False

            X = self.prepare_features(customers_df)
            y = customers_df['will_churn']

            # Scale features
            X_scaled = self.scaler.fit_transform(X)

            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_scaled, y)

            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump({'model': self.model, 'scaler': self.scaler}, f)

            self.is_trained = True
            print("Churn prediction model trained successfully!")
            return True

        except Exception as e:
            print(f"Error training churn model: {e}")
            return False

    def load_model(self):
        """Load trained churn model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.model = saved_data['model']
                    self.scaler = saved_data['scaler']
                    self.is_trained = True
                print("Churn model loaded successfully!")
                return True
        except Exception as e:
            print(f"Error loading churn model: {e}")
        return False

    def predict_churn(self, customers_df):
        """Predict churn for customers"""
        if not self.is_trained:
            if not self.load_model():
                print("Training new churn model...")
                if not self.train_model(customers_df):
                    # If training fails, return with basic risk scores
                    result_df = customers_df.copy()
                    np.random.seed(42)
                    result_df['churn_risk_score'] = np.random.uniform(20, 90, len(customers_df)).round(2)
                    result_df['risk_category'] = result_df['churn_risk_score'].apply(self.categorize_risk)
                    return result_df

        try:
            X = self.prepare_features(customers_df)
            X_scaled = self.scaler.transform(X)

            # Get churn probabilities
            churn_probabilities = self.model.predict_proba(X_scaled)[:, 1]

            # Add predictions to dataframe
            result_df = customers_df.copy()
            result_df['churn_risk_score'] = (churn_probabilities * 100).round(2)
            result_df['risk_category'] = result_df['churn_risk_score'].apply(self.categorize_risk)

            print("Churn risk predictions completed!")
            return result_df

        except Exception as e:
            print(f"Error predicting churn: {e}")
            print("Falling back to random scores for demo...")

            # Fallback: return with random scores
            result_df = customers_df.copy()
            np.random.seed(42)
            result_df['churn_risk_score'] = np.random.uniform(20, 90, len(customers_df)).round(2)
            result_df['risk_category'] = result_df['churn_risk_score'].apply(self.categorize_risk)
            return result_df

    def categorize_risk(self, score):
        """Categorize churn risk"""
        if score >= 70:
            return "High Risk"
        elif score >= 40:
            return "Medium Risk"
        else:
            return "Low Risk"

    def get_at_risk_customers(self, customers_df, threshold=70):
        """Get customers at high risk of churning"""
        # First predict churn to ensure the score column exists
        predicted_df = self.predict_churn(customers_df)

        # Check if churn_risk_score column exists
        if 'churn_risk_score' not in predicted_df.columns:
            print("Error: churn_risk_score column not found. Unable to identify at-risk customers.")
            return pd.DataFrame()

        # Filter customers at risk
        at_risk = predicted_df[predicted_df['churn_risk_score'] >= threshold]

        print(f"\n--- AT RISK CUSTOMERS (Score >= {threshold}%) ---")
        if len(at_risk) > 0:
            # Use only columns that exist
            display_cols = ['name', 'email', 'churn_risk_score', 'risk_category']
            available_cols = [col for col in display_cols if col in at_risk.columns]

            if available_cols:
                print(at_risk[available_cols].to_string(index=False))
            else:
                print("Required columns not available. Showing basic info:")
                basic_cols = [col for col in ['name', 'customer_id', 'churn_risk_score'] if col in at_risk.columns]
                if basic_cols:
                    print(at_risk[basic_cols].to_string(index=False))
                else:
                    print("No displayable columns found")
        else:
            print("No customers at high risk found.")

        return at_risk


# Demo function
def demo_churn_prediction():
    from lead_management import LeadManager

    # Load leads and generate customer data
    lm = LeadManager()
    leads = lm.leads_df

    predictor = ChurnPredictor()
    customers = predictor.generate_customer_data(leads)

    # Predict churn
    print("\n4. CHURN PREDICTION...")
    predictions = predictor.predict_churn(customers)

    print("\n--- CHURN RISK ANALYSIS ---")
    if 'churn_risk_score' in predictions.columns and 'risk_category' in predictions.columns:
        display_cols = ['name', 'churn_risk_score', 'risk_category']
        available_cols = [col for col in display_cols if col in predictions.columns]
        print(predictions[available_cols].to_string(index=False))
    else:
        print("Churn prediction columns not available.")

    # Show at-risk customers
    predictor.get_at_risk_customers(customers)


if __name__ == "__main__":
    demo_churn_prediction()
