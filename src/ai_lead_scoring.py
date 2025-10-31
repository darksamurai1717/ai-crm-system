import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os


class AILeadScorer:
    def __init__(self, model_path='models/lead_scorer.pkl'):
        self.model_path = model_path
        self.model = None
        self.label_encoders = {}
        self.is_trained = False

    def prepare_features(self, df):
        """Prepare features for ML model"""
        feature_df = df.copy()

        # Create engagement score based on interactions
        feature_df['days_since_created'] = pd.to_datetime('today') - pd.to_datetime(df['created_date'])
        feature_df['days_since_created'] = feature_df['days_since_created'].dt.days

        # Encode categorical variables
        categorical_cols = ['company', 'status']
        for col in categorical_cols:
            if col in feature_df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    feature_df[col + '_encoded'] = self.label_encoders[col].fit_transform(feature_df[col].astype(str))
                else:
                    feature_df[col + '_encoded'] = self.label_encoders[col].transform(feature_df[col].astype(str))

        # Select numerical features
        feature_cols = ['days_since_created', 'company_encoded']
        available_cols = [col for col in feature_cols if col in feature_df.columns]

        return feature_df[available_cols]

    def generate_training_data(self, leads_df):
        """Generate synthetic training data for demo purposes"""
        training_data = leads_df.copy()

        # Create synthetic conversion labels based on status
        training_data['converted'] = (training_data['status'] == 'Converted').astype(int)

        # Add some synthetic features for better ML performance
        np.random.seed(42)
        training_data['email_opens'] = np.random.randint(0, 20, len(training_data))
        training_data['website_visits'] = np.random.randint(0, 50, len(training_data))
        training_data['demo_requested'] = np.random.choice([0, 1], len(training_data), p=[0.7, 0.3])

        return training_data

    def train_model(self, leads_df):
        """Train the lead scoring model"""
        try:
            # Generate training data
            training_data = self.generate_training_data(leads_df)

            if len(training_data) < 5:
                print("Not enough data to train model. Need at least 5 leads.")
                return False

            # Prepare features
            X = self.prepare_features(training_data)

            # Add synthetic features to X
            X['email_opens'] = training_data['email_opens']
            X['website_visits'] = training_data['website_visits']
            X['demo_requested'] = training_data['demo_requested']

            y = training_data['converted']

            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X, y)

            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump({'model': self.model, 'encoders': self.label_encoders}, f)

            self.is_trained = True
            print("Lead scoring model trained successfully!")
            return True

        except Exception as e:
            print(f"Error training model: {e}")
            return False

    def load_model(self):
        """Load trained model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.model = saved_data['model']
                    self.label_encoders = saved_data['encoders']
                    self.is_trained = True
                print("Model loaded successfully!")
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False

    def score_leads(self, leads_df):
        """Score leads using trained model"""
        if not self.is_trained:
            if not self.load_model():
                print("No trained model available. Training new model...")
                if not self.train_model(leads_df):
                    return leads_df

        try:
            # Prepare features for prediction
            X = self.prepare_features(leads_df)

            # Add synthetic features for prediction (in real scenario, these would be real data)
            np.random.seed(42)
            X['email_opens'] = np.random.randint(0, 20, len(leads_df))
            X['website_visits'] = np.random.randint(0, 50, len(leads_df))
            X['demo_requested'] = np.random.choice([0, 1], len(leads_df), p=[0.7, 0.3])

            # Get probability predictions
            probabilities = self.model.predict_proba(X)[:, 1]  # Probability of conversion

            # Update leads dataframe with scores
            scored_leads = leads_df.copy()
            scored_leads['ai_score'] = (probabilities * 100).round(2)

            # Assign categories
            scored_leads['lead_category'] = scored_leads['ai_score'].apply(self.categorize_lead)

            print("Leads scored successfully!")
            return scored_leads

        except Exception as e:
            print(f"Error scoring leads: {e}")
            # Return original dataframe with default scores
            fallback_leads = leads_df.copy()
            fallback_leads['ai_score'] = np.random.uniform(20, 80, len(leads_df)).round(2)
            fallback_leads['lead_category'] = fallback_leads['ai_score'].apply(self.categorize_lead)
            return fallback_leads

    def categorize_lead(self, score):
        """Categorize lead based on score"""
        if score >= 70:
            return "Hot"
        elif score >= 40:
            return "Warm"
        else:
            return "Cold"


# Demo function
# Demo function - CORRECTED VERSION
def demo_ai_scoring():
    from lead_management import LeadManager

    # Load leads
    lm = LeadManager()
    leads = lm.leads_df

    if len(leads) == 0:
        print("No leads found. Please run lead_management.py first.")
        return

    # Score leads
    scorer = AILeadScorer()
    scored_leads = scorer.score_leads(leads)

    print("\n--- AI SCORED LEADS ---")
    # Only display columns that exist
    available_columns = []
    desired_columns = ['name', 'company', 'status', 'ai_score', 'lead_category']

    for col in desired_columns:
        if col in scored_leads.columns:
            available_columns.append(col)

    if available_columns:
        print(scored_leads[available_columns].to_string(index=False))
    else:
        print("Columns not available. Showing all data:")
        print(scored_leads.to_string(index=False))


if __name__ == "__main__":
    demo_ai_scoring()
