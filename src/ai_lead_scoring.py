"""
AI Lead Scoring System - Updated to use Real Dataset
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os


class LeadScorer:
    def __init__(self, dataset_path='data/dataset.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.df = None
        self.label_encoders = {}
        self.load_and_train()

    def load_and_train(self):
        """Load dataset and train lead scoring model"""
        try:
            if os.path.exists(self.dataset_path):
                self.df = pd.read_csv(self.dataset_path)
                print(f"✅ Loaded dataset with {len(self.df)} records for lead scoring")

                if len(self.df) > 20:
                    self._train_model()
                else:
                    print("⚠️ Not enough data to train lead scoring model")
            else:
                print(f"❌ Dataset not found at {self.dataset_path}")
        except Exception as e:
            print(f"Error loading dataset for lead scoring: {e}")

    def _train_model(self):
        """Train Random Forest model for lead scoring"""
        try:
            df = self.df.copy()

            # Prepare features
            df['revenue_potential'] = df['revenue_potential'].fillna(0)
            df['days_to_convert'] = df['days_to_convert'].fillna(30)

            # Encode categorical variables
            categorical_cols = ['source', 'industry', 'region', 'stage']

            for col in categorical_cols:
                if col in df.columns:
                    le = LabelEncoder()
                    df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le

            # Select features
            feature_cols = [
                'revenue_potential',
                'days_to_convert',
                'source_encoded',
                'industry_encoded',
                'region_encoded',
                'stage_encoded'
            ]

            # Filter available features
            available_features = [col for col in feature_cols if col in df.columns]

            X = df[available_features]
            y = df['converted']

            # Train model
            if len(X) > 10:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )

                self.model = RandomForestClassifier(
                    n_estimators=100,
                    random_state=42,
                    max_depth=10
                )
                self.model.fit(X_train, y_train)

                accuracy = self.model.score(X_test, y_test)
                print(f"✅ Lead scoring model trained with {accuracy * 100:.1f}% accuracy")
        except Exception as e:
            print(f"Error training lead scoring model: {e}")

    def calculate_score(self, lead_data):
        """Calculate lead score (0-100)"""
        if self.model is None:
            # Use rule-based fallback scoring
            return self._rule_based_score(lead_data)

        try:
            # Prepare features
            features = {}
            features['revenue_potential'] = lead_data.get('revenue_potential', 0)
            features['days_to_convert'] = lead_data.get('days_to_convert', 30)

            # Encode categorical features
            for col in ['source', 'industry', 'region', 'stage']:
                if col in self.label_encoders:
                    value = lead_data.get(col, 'Unknown')
                    try:
                        features[col + '_encoded'] = self.label_encoders[col].transform([value])[0]
                    except:
                        features[col + '_encoded'] = 0

            # Create feature array
            feature_array = [[
                features.get('revenue_potential', 0),
                features.get('days_to_convert', 30),
                features.get('source_encoded', 0),
                features.get('industry_encoded', 0),
                features.get('region_encoded', 0),
                features.get('stage_encoded', 0)
            ]]

            # Predict probability
            probability = self.model.predict_proba(feature_array)[0][1]
            score = int(probability * 100)

            return min(max(score, 0), 100)
        except Exception as e:
            print(f"Error calculating ML score: {e}")
            return self._rule_based_score(lead_data)

    def _rule_based_score(self, lead_data):
        """Fallback rule-based scoring"""
        score = 50  # Base score

        # Revenue potential impact
        revenue = lead_data.get('revenue_potential', 0)
        if revenue > 60000:
            score += 25
        elif revenue > 45000:
            score += 15
        elif revenue > 30000:
            score += 10

        # Stage impact
        stage = lead_data.get('stage', '')
        if stage == 'Qualified':
            score += 20
        elif stage == 'Contacted':
            score += 10
        elif stage == 'Converted':
            score = 100

        # Source impact
        source = lead_data.get('source', '')
        if source == 'Referral':
            score += 10
        elif source == 'LinkedIn':
            score += 5

        # Industry impact (high-value industries)
        industry = lead_data.get('industry', '')
        if industry in ['IT', 'Finance', 'Healthcare']:
            score += 5

        return min(max(score, 0), 100)

    def get_hot_leads(self, threshold=70):
        """Get leads with score above threshold"""
        if self.df is None or self.df.empty:
            return []

        hot_leads = []

        for _, row in self.df.iterrows():
            if row['converted'] == 0:  # Only unconverted leads
                lead_data = {
                    'revenue_potential': row['revenue_potential'],
                    'days_to_convert': row.get('days_to_convert', 30),
                    'source': row['source'],
                    'industry': row['industry'],
                    'region': row['region'],
                    'stage': row['stage']
                }

                score = self.calculate_score(lead_data)

                if score >= threshold:
                    hot_leads.append({
                        'id': row['lead_id'],
                        'name': row['name'],
                        'company': row['industry'],
                        'score': score,
                        'revenue_potential': row['revenue_potential']
                    })

        return sorted(hot_leads, key=lambda x: x['score'], reverse=True)

    def get_hot_leads_count(self, threshold=70):
        """Get count of hot leads"""
        return len(self.get_hot_leads(threshold))

    def score_all_leads(self):
        """Score all leads in the dataset"""
        if self.df is None or self.df.empty:
            return []

        scored_leads = []

        for _, row in self.df.iterrows():
            lead_data = {
                'revenue_potential': row['revenue_potential'],
                'days_to_convert': row.get('days_to_convert', 30),
                'source': row['source'],
                'industry': row['industry'],
                'region': row['region'],
                'stage': row['stage']
            }

            score = self.calculate_score(lead_data)

            scored_leads.append({
                'lead_id': row['lead_id'],
                'name': row['name'],
                'email': row['email'],
                'company': row['industry'],
                'score': score,
                'revenue_potential': row['revenue_potential'],
                'stage': row['stage'],
                'converted': row['converted'] == 1
            })

        return sorted(scored_leads, key=lambda x: x['score'], reverse=True)

    def get_score_distribution(self):
        """Get distribution of lead scores"""
        if self.df is None or self.df.empty:
            return {'Hot (70-100)': 0, 'Warm (40-69)': 0, 'Cold (0-39)': 0}

        all_scores = []
        for _, row in self.df.iterrows():
            if row['converted'] == 0:  # Only unconverted leads
                lead_data = {
                    'revenue_potential': row['revenue_potential'],
                    'days_to_convert': row.get('days_to_convert', 30),
                    'source': row['source'],
                    'industry': row['industry'],
                    'region': row['region'],
                    'stage': row['stage']
                }
                score = self.calculate_score(lead_data)
                all_scores.append(score)

        hot = sum(1 for s in all_scores if s >= 70)
        warm = sum(1 for s in all_scores if 40 <= s < 70)
        cold = sum(1 for s in all_scores if s < 40)

        return {
            'Hot (70-100)': hot,
            'Warm (40-69)': warm,
            'Cold (0-39)': cold
        }


