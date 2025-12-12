"""
Lead Management System - Updated to use Real Dataset
"""
import pandas as pd
from datetime import datetime, timedelta
import os


class LeadManager:
    def __init__(self, dataset_path='data/dataset.csv'):
        self.dataset_path = dataset_path
        self.leads_df = None
        self.load_dataset()

    def load_dataset(self):
        """Load real dataset from CSV"""
        try:
            if os.path.exists(self.dataset_path):
                self.leads_df = pd.read_csv(self.dataset_path)
                print(f"✅ Loaded {len(self.leads_df)} leads from dataset")
            else:
                print(f"❌ Dataset not found at {self.dataset_path}")
                self.leads_df = pd.DataFrame()
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.leads_df = pd.DataFrame()

    def get_all_leads(self):
        """Get all leads from dataset"""
        if self.leads_df is None or self.leads_df.empty:
            return []

        leads = []
        for _, row in self.leads_df.iterrows():
            leads.append({
                'id': row['lead_id'],
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone'],
                'company': row['industry'],
                'status': row['stage'],
                'score': int(row['revenue_potential'] / 1000) if pd.notna(row['revenue_potential']) else 0,
                'revenue_potential': row['revenue_potential'],
                'created_date': row.get('created_date', ''),
                'converted': row['converted'] == 1
            })
        return leads

    def get_lead_by_id(self, lead_id):
        """Get specific lead by ID"""
        if self.leads_df is None or self.leads_df.empty:
            return None

        lead_row = self.leads_df[self.leads_df['lead_id'] == lead_id]
        if lead_row.empty:
            return None

        row = lead_row.iloc[0]
        return {
            'id': row['lead_id'],
            'name': row['name'],
            'email': row['email'],
            'phone': row['phone'],
            'company': row['industry'],
            'status': row['stage'],
            'score': int(row['revenue_potential'] / 1000) if pd.notna(row['revenue_potential']) else 0,
            'revenue_potential': row['revenue_potential'],
            'created_date': row.get('created_date', ''),
            'converted': row['converted'] == 1
        }

    def get_hot_leads(self, threshold=50000):
        """Get leads with high revenue potential"""
        if self.leads_df is None or self.leads_df.empty:
            return []

        hot_leads = self.leads_df[
            (self.leads_df['revenue_potential'] >= threshold) &
            (self.leads_df['converted'] == 0)
            ]
        return len(hot_leads)

    def get_conversion_rate(self):
        """Calculate conversion rate from dataset"""
        if self.leads_df is None or self.leads_df.empty:
            return 0.0

        total = len(self.leads_df)
        converted = len(self.leads_df[self.leads_df['converted'] == 1])
        return round((converted / total) * 100, 1) if total > 0 else 0.0

    def get_total_revenue(self):
        """Calculate total revenue from converted leads"""
        if self.leads_df is None or self.leads_df.empty:
            return 0

        converted_leads = self.leads_df[self.leads_df['converted'] == 1]
        total = converted_leads['deal_amount'].sum()
        return int(total) if pd.notna(total) else 0

    def get_pipeline_distribution(self):
        """Get distribution of leads by stage"""
        if self.leads_df is None or self.leads_df.empty:
            return {}

        distribution = self.leads_df['stage'].value_counts().to_dict()
        return distribution

    def get_recent_activities(self, limit=10):
        """Generate recent activities from dataset"""
        if self.leads_df is None or self.leads_df.empty:
            return []

        activities = []
        recent_leads = self.leads_df.sort_values('last_login', ascending=False).head(limit)

        for _, row in recent_leads.iterrows():
            if row['converted'] == 1:
                activities.append({
                    'type': 'conversion',
                    'lead_name': row['name'],
                    'company': row['industry'],
                    'amount': row['deal_amount'],
                    'timestamp': row['last_login']
                })
            elif row['stage'] == 'Qualified':
                activities.append({
                    'type': 'qualified',
                    'lead_name': row['name'],
                    'company': row['industry'],
                    'timestamp': row['last_login']
                })
            elif row['stage'] == 'Contacted':
                activities.append({
                    'type': 'contact',
                    'lead_name': row['name'],
                    'company': row['industry'],
                    'timestamp': row['last_login']
                })

        return activities[:limit]

    def get_stats(self):
        """Get comprehensive statistics"""
        if self.leads_df is None or self.leads_df.empty:
            return {
                'total_leads': 0,
                'converted': 0,
                'conversion_rate': 0,
                'total_revenue': 0,
                'hot_leads': 0,
                'avg_deal_size': 0
            }

        converted_leads = self.leads_df[self.leads_df['converted'] == 1]

        return {
            'total_leads': len(self.leads_df),
            'converted': len(converted_leads),
            'conversion_rate': self.get_conversion_rate(),
            'total_revenue': self.get_total_revenue(),
            'hot_leads': self.get_hot_leads(),
            'avg_deal_size': int(converted_leads['deal_amount'].mean()) if len(converted_leads) > 0 else 0
        }