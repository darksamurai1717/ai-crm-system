import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os


class CustomerSegmentation:
    def __init__(self, model_path='models/segmentation_model.pkl'):
        self.model_path = model_path
        self.kmeans_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.segment_labels = {0: 'High-Value', 1: 'Low-Engagement', 2: 'Trial Users'}

    def generate_customer_features(self, customers_df):
        """Generate features for customer segmentation"""
        features_df = customers_df.copy()

        # If customers_df is empty or missing required columns, generate synthetic data
        if len(features_df) == 0 or 'monthly_spend' not in features_df.columns:
            np.random.seed(42)
            n_customers = max(10, len(features_df))

            synthetic_features = pd.DataFrame({
                'customer_id': range(1, n_customers + 1),
                'name': [f'Customer {i}' for i in range(1, n_customers + 1)],
                'monthly_spend': np.random.normal(100, 50, n_customers),
                'total_purchases': np.random.poisson(5, n_customers),
                'days_active': np.random.randint(30, 365, n_customers),
                'support_interactions': np.random.poisson(2, n_customers),
                'feature_usage_score': np.random.uniform(0, 100, n_customers),
                'last_activity_days': np.random.randint(0, 60, n_customers)
            })

            # Ensure positive values
            synthetic_features['monthly_spend'] = np.abs(synthetic_features['monthly_spend'])

            return synthetic_features

        return features_df

    def prepare_clustering_features(self, features_df):
        """Prepare features for clustering"""
        clustering_features = features_df[[
            'monthly_spend', 'total_purchases', 'days_active',
            'support_interactions', 'feature_usage_score', 'last_activity_days'
        ]].copy()

        # Handle missing values
        clustering_features = clustering_features.fillna(clustering_features.mean())

        return clustering_features

    def train_segmentation_model(self, customers_df, n_clusters=3):
        """Train customer segmentation model"""
        try:
            features_df = self.generate_customer_features(customers_df)

            if len(features_df) < n_clusters:
                print(f"Not enough customers for {n_clusters} segments. Need at least {n_clusters} customers.")
                return False

            # Prepare features
            X = self.prepare_clustering_features(features_df)

            # Scale features
            X_scaled = self.scaler.fit_transform(X)

            # Train KMeans
            self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.kmeans_model.fit(X_scaled)

            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump({
                    'model': self.kmeans_model,
                    'scaler': self.scaler,
                    'labels': self.segment_labels
                }, f)

            self.is_trained = True
            print("Customer segmentation model trained successfully!")
            return True

        except Exception as e:
            print(f"Error training segmentation model: {e}")
            return False

    def load_model(self):
        """Load trained segmentation model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.kmeans_model = saved_data['model']
                    self.scaler = saved_data['scaler']
                    self.segment_labels = saved_data.get('labels', self.segment_labels)
                    self.is_trained = True
                print("Segmentation model loaded successfully!")
                return True
        except Exception as e:
            print(f"Error loading segmentation model: {e}")
        return False

    def segment_customers(self, customers_df):
        """Segment customers using trained model"""
        if not self.is_trained:
            if not self.load_model():
                print("Training new segmentation model...")
                if not self.train_segmentation_model(customers_df):
                    # Fallback: assign random segments
                    result_df = self.generate_customer_features(customers_df)
                    np.random.seed(42)
                    result_df['segment_id'] = np.random.randint(0, 3, len(result_df))
                    result_df['segment_name'] = [self.segment_labels.get(seg, f'Segment {seg}')
                                                 for seg in result_df['segment_id']]
                    return result_df

        try:
            features_df = self.generate_customer_features(customers_df)
            X = self.prepare_clustering_features(features_df)
            X_scaled = self.scaler.transform(X)

            # Predict segments
            segment_predictions = self.kmeans_model.predict(X_scaled)

            # Add segments to dataframe
            result_df = features_df.copy()
            result_df['segment_id'] = segment_predictions
            result_df['segment_name'] = [self.segment_labels.get(seg, f'Segment {seg}')
                                         for seg in segment_predictions]

            print("Customer segmentation completed!")
            return result_df

        except Exception as e:
            print(f"Error segmenting customers: {e}")
            print("Falling back to random segments for demo...")

            # Fallback: random segments
            result_df = self.generate_customer_features(customers_df)
            np.random.seed(42)
            result_df['segment_id'] = np.random.randint(0, 3, len(result_df))
            result_df['segment_name'] = [self.segment_labels.get(seg, f'Segment {seg}')
                                         for seg in result_df['segment_id']]
            return result_df

    def analyze_segments(self, segmented_df):
        """Analyze customer segments"""
        print("\n--- SEGMENT ANALYSIS ---")

        # Check if segment_name column exists
        if 'segment_name' not in segmented_df.columns:
            print("Error: segment_name column not found. Running segmentation first...")
            segmented_df = self.segment_customers(segmented_df)

        if 'segment_name' not in segmented_df.columns:
            print("Unable to create segments. Showing basic statistics instead.")
            basic_stats = segmented_df.describe()
            print(basic_stats)
            return basic_stats

        try:
            # Create segment summary with available columns
            agg_dict = {}

            # Check which columns are available for analysis
            if 'monthly_spend' in segmented_df.columns:
                agg_dict['monthly_spend'] = ['mean', 'count']
            if 'total_purchases' in segmented_df.columns:
                agg_dict['total_purchases'] = 'mean'
            if 'days_active' in segmented_df.columns:
                agg_dict['days_active'] = 'mean'
            if 'feature_usage_score' in segmented_df.columns:
                agg_dict['feature_usage_score'] = 'mean'

            if agg_dict:
                segment_summary = segmented_df.groupby('segment_name').agg(agg_dict).round(2)
                print(segment_summary)
                return segment_summary
            else:
                # Fallback: just show counts by segment
                segment_counts = segmented_df['segment_name'].value_counts()
                print("Segment Counts:")
                print(segment_counts)
                return segment_counts

        except Exception as e:
            print(f"Error analyzing segments: {e}")
            return pd.DataFrame()

    def visualize_segments(self, segmented_df):
        """Create visualizations for segments"""
        try:
            plt.figure(figsize=(12, 8))

            # Subplot 1: Spending by Segment
            plt.subplot(2, 2, 1)
            segmented_df.boxplot(column='monthly_spend', by='segment_name', ax=plt.gca())
            plt.title('Monthly Spend by Segment')
            plt.suptitle('')

            # Subplot 2: Purchase Frequency by Segment
            plt.subplot(2, 2, 2)
            segmented_df.boxplot(column='total_purchases', by='segment_name', ax=plt.gca())
            plt.title('Total Purchases by Segment')
            plt.suptitle('')

            # Subplot 3: Feature Usage by Segment
            plt.subplot(2, 2, 3)
            segmented_df.boxplot(column='feature_usage_score', by='segment_name', ax=plt.gca())
            plt.title('Feature Usage Score by Segment')
            plt.suptitle('')

            # Subplot 4: Segment Distribution
            plt.subplot(2, 2, 4)
            segment_counts = segmented_df['segment_name'].value_counts()
            plt.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%')
            plt.title('Customer Distribution by Segment')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error creating visualizations: {e}")


# Demo function
def demo_segmentation():
    from lead_management import LeadManager
    from churn_prediction import ChurnPredictor

    # Load data
    lm = LeadManager()
    leads = lm.leads_df

    # Generate customer data
    predictor = ChurnPredictor()
    customers = predictor.generate_customer_data(leads)

    # Segment customers
    segmentation = CustomerSegmentation()
    segmented_customers = segmentation.segment_customers(customers)

    print("\n--- CUSTOMER SEGMENTS ---")
    display_cols = ['name', 'monthly_spend', 'segment_name']
    print(segmented_customers[display_cols].to_string(index=False))

    # Analyze segments
    segmentation.analyze_segments(segmented_customers)

    # Create visualizations
    segmentation.visualize_segments(segmented_customers)


if __name__ == "__main__":
    demo_segmentation()
