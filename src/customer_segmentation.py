"""
Customer Segmentation System - Updated to use Real Dataset
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os


class CustomerSegmenter:
    def __init__(self, dataset_path='data/dataset.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.scaler = None
        self.df = None
        self.segments = None
        self.load_and_segment()

    def load_and_segment(self):
        """Load dataset and perform K-Means clustering"""
        try:
            if os.path.exists(self.dataset_path):
                self.df = pd.read_csv(self.dataset_path)
                print(f"✅ Loaded dataset with {len(self.df)} records for segmentation")

                # Only segment converted customers
                converted_df = self.df[self.df['converted'] == 1].copy()

                if len(converted_df) > 5:
                    self._perform_clustering(converted_df)
                else:
                    print("⚠️ Not enough converted customers for segmentation")
            else:
                print(f"❌ Dataset not found at {self.dataset_path}")
        except Exception as e:
            print(f"Error loading dataset for segmentation: {e}")

    def _perform_clustering(self, df):
        """Perform K-Means clustering on customer data"""
        try:
            # Prepare features
            df['avg_monthly_spend'] = df['avg_monthly_spend'].fillna(0)
            df['revenue_potential'] = df['revenue_potential'].fillna(0)
            df['tenure_months'] = df['tenure_months'].fillna(0)

            # Features for clustering
            features = ['avg_monthly_spend', 'revenue_potential', 'tenure_months']
            X = df[features]

            # Standardize features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)

            # K-Means clustering (3 segments)
            n_clusters = min(3, len(df))
            self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            df['segment'] = self.model.fit_predict(X_scaled)

            # Analyze segments
            self.segments = self._analyze_segments(df)

            print(f"✅ Created {n_clusters} customer segments")
        except Exception as e:
            print(f"Error performing clustering: {e}")

    def _analyze_segments(self, df):
        """Analyze characteristics of each segment"""
        segments_info = {}

        for segment_id in df['segment'].unique():
            segment_data = df[df['segment'] == segment_id]

            avg_spend = segment_data['avg_monthly_spend'].mean()
            avg_revenue = segment_data['revenue_potential'].mean()

            # Categorize segment
            if avg_spend > 6000:
                label = "Premium"
            elif avg_spend > 4500:
                label = "Growth"
            else:
                label = "Standard"

            segments_info[int(segment_id)] = {
                'label': label,
                'count': len(segment_data),
                'avg_spend': round(avg_spend, 2),
                'avg_revenue': round(avg_revenue, 2),
                'customers': segment_data['name'].tolist()
            }

        return segments_info

    def get_segment_distribution(self):
        """Get distribution of customers across segments"""
        if self.segments is None:
            return {'Premium': 0, 'Growth': 0, 'Standard': 0}

        distribution = {'Premium': 0, 'Growth': 0, 'Standard': 0}

        for segment_info in self.segments.values():
            label = segment_info['label']
            distribution[label] = distribution.get(label, 0) + segment_info['count']

        return distribution

    def get_segment_details(self):
        """Get detailed information about each segment"""
        if self.segments is None:
            return []

        details = []
        for segment_id, info in self.segments.items():
            details.append({
                'id': segment_id,
                'name': info['label'],
                'count': info['count'],
                'avg_spend': info['avg_spend'],
                'avg_revenue': info['avg_revenue'],
                'percentage': 0  # Will be calculated in the endpoint
            })

        return details

    def predict_segment(self, customer_data):
        """Predict segment for a new customer"""
        if self.model is None or self.scaler is None:
            # Rule-based fallback
            spend = customer_data.get('avg_monthly_spend', 0)
            if spend > 6000:
                return "Premium"
            elif spend > 4500:
                return "Growth"
            else:
                return "Standard"

        try:
            features = [[
                customer_data.get('avg_monthly_spend', 0),
                customer_data.get('revenue_potential', 0),
                customer_data.get('tenure_months', 0)
            ]]

            features_scaled = self.scaler.transform(features)
            segment_id = self.model.predict(features_scaled)[0]

            return self.segments[int(segment_id)]['label']
        except:
            return "Standard"

    def get_segment_insights(self):
        """Get insights about customer segments"""
        if self.segments is None or self.df is None:
            return {
                'total_segments': 0,
                'largest_segment': 'N/A',
                'most_valuable': 'N/A',
                'recommendations': []
            }

        # Find largest segment
        largest = max(self.segments.items(), key=lambda x: x[1]['count'])

        # Find most valuable segment
        most_valuable = max(self.segments.items(), key=lambda x: x[1]['avg_revenue'])

        return {
            'total_segments': len(self.segments),
            'largest_segment': largest[1]['label'],
            'largest_count': largest[1]['count'],
            'most_valuable': most_valuable[1]['label'],
            'most_valuable_revenue': most_valuable[1]['avg_revenue'],
            'recommendations': [
                f"Focus upselling efforts on {largest[1]['label']} segment ({largest[1]['count']} customers)",
                f"Prioritize retention for {most_valuable[1]['label']} segment (highest LTV)",
                "Implement tiered pricing based on segment characteristics"
            ]
        }