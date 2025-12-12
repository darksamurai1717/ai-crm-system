"""
Churn Prediction System - Updated to use Real Dataset
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os


class ChurnPredictor:
    def __init__(self, dataset_path='data/dataset.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.df = None
        self.load_and_train()

    def load_and_train(self):
        """Load dataset and train churn prediction model"""
        try:
            if os.path.exists(self.dataset_path):
                self.df = pd.read_csv(self.dataset_path)
                print(f"✅ Loaded dataset with {len(self.df)} records for churn prediction")

                # Train model on converted customers only
                converted_df = self.df[self.df['converted'] == 1].copy()

                if len(converted_df) > 10:
                    self._train_model(converted_df)
                else:
                    print("⚠️ Not enough converted customers to train churn model")
            else:
                print(f"❌ Dataset not found at {self.dataset_path}")
        except Exception as e:
            print(f"Error loading dataset for churn prediction: {e}")

    def _train_model(self, df):
        """Train Random Forest model for churn prediction"""
        try:
            # Prepare features
            df['tenure_months'] = df['tenure_months'].fillna(0)
            df['avg_monthly_spend'] = df['avg_monthly_spend'].fillna(0)
            df['satisfaction_score'] = df['satisfaction_score'].fillna(7)
            df['num_support_tickets'] = df['num_support_tickets'].fillna(0)

            # Feature engineering
            features = ['tenure_months', 'avg_monthly_spend', 'satisfaction_score', 'num_support_tickets']
            X = df[features]
            y = df['churned']

            # Train model
            if len(X) > 5:
                self.model = RandomForestClassifier(n_estimators=50, random_state=42)
                self.model.fit(X, y)
                print("✅ Churn prediction model trained successfully")
        except Exception as e:
            print(f"Error training churn model: {e}")

    def get_churn_rate(self):
        """Calculate actual churn rate from dataset"""
        if self.df is None or self.df.empty:
            return 0.0

        converted_customers = self.df[self.df['converted'] == 1]
        if len(converted_customers) == 0:
            return 0.0

        churned = len(converted_customers[converted_customers['churned'] == 1])
        total = len(converted_customers)

        return round((churned / total) * 100, 1)

    def get_at_risk_customers(self):
        """Get count of customers at high risk of churning"""
        if self.df is None or self.df.empty:
            return 0

        # Customers with low satisfaction or high support tickets
        converted_customers = self.df[self.df['converted'] == 1]

        at_risk = converted_customers[
            (converted_customers['satisfaction_score'] < 7) |
            (converted_customers['num_support_tickets'] > 2) |
            (converted_customers['churned'] == 1)
            ]

        return len(at_risk)

    def predict_churn_risk(self, customer_data):
        """Predict churn risk for a specific customer"""
        if self.model is None:
            # Use rule-based fallback
            score = customer_data.get('satisfaction_score', 7)
            tickets = customer_data.get('num_support_tickets', 0)
            tenure = customer_data.get('tenure_months', 0)

            risk_score = 0
            if score < 6:
                risk_score += 40
            elif score < 8:
                risk_score += 20

            if tickets > 3:
                risk_score += 30
            elif tickets > 1:
                risk_score += 15

            if tenure < 6:
                risk_score += 20

            return min(risk_score, 100)

        try:
            features = [[
                customer_data.get('tenure_months', 0),
                customer_data.get('avg_monthly_spend', 0),
                customer_data.get('satisfaction_score', 7),
                customer_data.get('num_support_tickets', 0)
            ]]

            probability = self.model.predict_proba(features)[0][1]
            return int(probability * 100)
        except:
            return 0

    def get_churn_distribution(self):
        """Get distribution of churn risk levels"""
        if self.df is None or self.df.empty:
            return {'Low': 0, 'Medium': 0, 'High': 0}

        converted_customers = self.df[self.df['converted'] == 1].copy()

        if len(converted_customers) == 0:
            return {'Low': 0, 'Medium': 0, 'High': 0}

        # Calculate risk scores
        converted_customers['risk_score'] = 0

        # Low satisfaction increases risk
        converted_customers.loc[converted_customers['satisfaction_score'] < 7, 'risk_score'] += 40
        converted_customers.loc[
            (converted_customers['satisfaction_score'] >= 7) &
            (converted_customers['satisfaction_score'] < 8),
            'risk_score'
        ] += 20

        # High support tickets increase risk
        converted_customers.loc[converted_customers['num_support_tickets'] > 2, 'risk_score'] += 30
        converted_customers.loc[
            (converted_customers['num_support_tickets'] > 0) &
            (converted_customers['num_support_tickets'] <= 2),
            'risk_score'
        ] += 15

        # Already churned
        converted_customers.loc[converted_customers['churned'] == 1, 'risk_score'] = 100

        # Categorize
        low_risk = len(converted_customers[converted_customers['risk_score'] < 30])
        medium_risk = len(converted_customers[
                              (converted_customers['risk_score'] >= 30) &
                              (converted_customers['risk_score'] < 60)
                              ])
        high_risk = len(converted_customers[converted_customers['risk_score'] >= 60])

        return {
            'Low': low_risk,
            'Medium': medium_risk,
            'High': high_risk
        }

    def get_churned_customers(self):
        """Get list of churned customers"""
        if self.df is None or self.df.empty:
            return []

        churned = self.df[self.df['churned'] == 1]

        return [{
            'name': row['name'],
            'company': row['industry'],
            'tenure': row['tenure_months'],
            'last_spend': row['avg_monthly_spend'],
            'reason': 'Low satisfaction' if row['satisfaction_score'] < 7 else 'Support issues'
        } for _, row in churned.iterrows()]