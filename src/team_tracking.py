"""
Team Tracking System - Updated to use Real Dataset
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


class TeamTracker:
    def __init__(self, dataset_path='data/dataset.csv'):
        self.dataset_path = dataset_path
        self.df = None
        self.load_dataset()

    def load_dataset(self):
        """Load real dataset from CSV"""
        try:
            if os.path.exists(self.dataset_path):
                self.df = pd.read_csv(self.dataset_path)
                print(f"✅ Loaded dataset with {len(self.df)} records for team tracking")
            else:
                print(f"❌ Dataset not found at {self.dataset_path}")
        except Exception as e:
            print(f"Error loading dataset for team tracking: {e}")

    def get_team_members(self):
        """Get unique sales reps from dataset"""
        if self.df is None or self.df.empty:
            return []

        reps = self.df['sales_rep'].unique()
        return [rep for rep in reps if pd.notna(rep)]

    def get_rep_performance(self, rep_name):
        """Get performance metrics for a specific sales rep"""
        if self.df is None or self.df.empty:
            return None

        rep_data = self.df[self.df['sales_rep'] == rep_name]

        if len(rep_data) == 0:
            return None

        # Get unique rep_id and performance_score
        rep_id = rep_data['rep_id'].iloc[0] if 'rep_id' in rep_data.columns else 'N/A'
        performance_score = rep_data['performance_score'].iloc[0] if 'performance_score' in rep_data.columns else 0

        # Calculate metrics
        total_leads = len(rep_data)
        converted = len(rep_data[rep_data['converted'] == 1])
        conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0

        # Revenue from converted deals
        converted_data = rep_data[rep_data['converted'] == 1]
        total_revenue = converted_data['deal_amount'].sum() if len(converted_data) > 0 else 0

        # Get region (most common)
        region = rep_data['region'].mode()[0] if 'region' in rep_data.columns else 'Unknown'

        # Active deals (qualified or contacted, not converted or lost)
        active_deals = len(rep_data[
                               (rep_data['stage'].isin(['Qualified', 'Contacted'])) &
                               (rep_data['converted'] == 0)
                               ])

        return {
            'name': rep_name,
            'rep_id': rep_id,
            'region': region,
            'total_leads': total_leads,
            'converted': converted,
            'conversion_rate': round(conversion_rate, 1),
            'total_revenue': int(total_revenue),
            'performance_score': round(float(performance_score), 1),
            'active_deals': active_deals,
            'avg_deal_size': int(total_revenue / converted) if converted > 0 else 0
        }

    def get_all_team_performance(self):
        """Get performance metrics for all team members"""
        team_members = self.get_team_members()

        performance_data = []
        for rep in team_members:
            rep_perf = self.get_rep_performance(rep)
            if rep_perf:
                performance_data.append(rep_perf)

        # Sort by performance score
        return sorted(performance_data, key=lambda x: x['performance_score'], reverse=True)

    def get_team_stats(self):
        """Get overall team statistics"""
        if self.df is None or self.df.empty:
            return {
                'total_members': 0,
                'avg_performance': 0,
                'total_revenue': 0,
                'avg_conversion': 0,
                'target_achievement': 0
            }

        team_performance = self.get_all_team_performance()

        if len(team_performance) == 0:
            return {
                'total_members': 0,
                'avg_performance': 0,
                'total_revenue': 0,
                'avg_conversion': 0,
                'target_achievement': 0
            }

        total_revenue = sum(rep['total_revenue'] for rep in team_performance)
        avg_performance = np.mean([rep['performance_score'] for rep in team_performance])
        avg_conversion = np.mean([rep['conversion_rate'] for rep in team_performance])

        # Calculate target achievement (assuming target is 80% conversion)
        target_achievement = (avg_conversion / 80) * 100

        return {
            'total_members': len(team_performance),
            'avg_performance': round(avg_performance, 1),
            'total_revenue': int(total_revenue),
            'avg_conversion': round(avg_conversion, 1),
            'target_achievement': round(min(target_achievement, 100), 1)
        }

    def get_top_performers(self, limit=3):
        """Get top performing sales reps"""
        team_performance = self.get_all_team_performance()
        return team_performance[:limit]

    def get_region_distribution(self):
        """Get lead distribution by region"""
        if self.df is None or self.df.empty:
            return {}

        return self.df['region'].value_counts().to_dict()

    def get_team_activities(self, limit=10):
        """Generate recent team activities from dataset"""
        if self.df is None or self.df.empty:
            return []

        activities = []

        # Recent conversions
        recent_conversions = self.df[self.df['converted'] == 1].sort_values(
            'close_date', ascending=False
        ).head(limit)

        for _, row in recent_conversions.iterrows():
            activities.append({
                'type': 'conversion',
                'rep': row['sales_rep'],
                'lead': row['name'],
                'company': row['industry'],
                'amount': row['deal_amount'],
                'timestamp': row['close_date']
            })

        # Recent qualifications
        recent_qualified = self.df[
            (self.df['stage'] == 'Qualified') &
            (self.df['converted'] == 0)
            ].head(limit // 2)

        for _, row in recent_qualified.iterrows():
            activities.append({
                'type': 'qualified',
                'rep': row['sales_rep'],
                'lead': row['name'],
                'company': row['industry'],
                'timestamp': row['last_login']
            })

        return activities[:limit]

    def get_workload_balance(self):
        """Analyze workload distribution across team"""
        if self.df is None or self.df.empty:
            return {'balanced': True, 'recommendation': 'Team workload is optimal'}

        team_performance = self.get_all_team_performance()

        if len(team_performance) == 0:
            return {'balanced': True, 'recommendation': 'No team data available'}

        lead_counts = [rep['total_leads'] for rep in team_performance]
        avg_leads = np.mean(lead_counts)
        std_leads = np.std(lead_counts)

        # Check if distribution is balanced (within 20% of mean)
        balanced = std_leads < (avg_leads * 0.2)

        if balanced:
            recommendation = "Workload is well balanced across the team"
        else:
            max_leads = max(lead_counts)
            min_leads = min(lead_counts)
            diff_percent = ((max_leads - min_leads) / avg_leads) * 100
            recommendation = f"Consider redistributing {int(diff_percent)}% of leads from top to lower-loaded reps"

        return {
            'balanced': balanced,
            'avg_leads_per_rep': round(avg_leads, 1),
            'std_deviation': round(std_leads, 1),
            'recommendation': recommendation
        }

    def get_performance_trends(self):
        """Get performance trends over time"""
        if self.df is None or self.df.empty:
            return []

        # Group by sales rep and calculate monthly metrics
        team_members = self.get_team_members()

        trends = []
        for rep in team_members:
            rep_data = self.df[self.df['sales_rep'] == rep]

            # Calculate recent vs historical performance
            recent_conversion = len(rep_data[
                                        (rep_data['converted'] == 1) &
                                        (pd.to_datetime(rep_data['close_date'], errors='coerce') >=
                                         pd.Timestamp.now() - pd.Timedelta(days=30))
                                        ])

            total_conversion = len(rep_data[rep_data['converted'] == 1])

            trend_direction = 'up' if recent_conversion > (total_conversion / 3) else 'stable'

            trends.append({
                'rep': rep,
                'trend': trend_direction,
                'recent_conversions': recent_conversion,
                'total_conversions': total_conversion
            })

        return trends