import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pickle
import os


class SalesTracker:
    def __init__(self, model_path='models/sales_forecast_model.pkl'):
        self.model_path = model_path
        self.forecast_model = None
        self.scaler = StandardScaler()
        self.is_trained = False

    def generate_sales_data(self, leads_df):
        """Generate synthetic sales/deals data from leads"""
        import random
        from datetime import datetime, timedelta

        deals = []

        for idx, lead in leads_df.iterrows():
            # Create 0-2 deals per lead
            num_deals = random.randint(0, 2)

            for deal_num in range(num_deals):
                deal = {
                    'deal_id': f"DEAL-{idx}-{deal_num}",
                    'deal_name': f"{lead['company']} - {['Product Sale', 'Service Contract', 'Consulting'][deal_num % 3]}",
                    # FIXED: Added deal_name
                    'lead_name': lead['name'],
                    'company': lead['company'],
                    'deal_value': random.randint(5000, 150000),
                    'deal_stage': random.choice(
                        ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Won', 'Lost']),
                    'probability': random.randint(10, 90),
                    'expected_close_date': (datetime.now() + timedelta(days=random.randint(-30, 90))).strftime(
                        '%Y-%m-%d'),
                    'created_date': lead['created_date'],
                    'sales_rep': random.choice(
                        ['Alice Johnson', 'Bob Wilson', 'Carol Davis', 'David Brown', 'Eva Martinez'])
                }
                deals.append(deal)

        # Ensure at least some sample deals exist
        if len(deals) == 0:
            for i in range(10):
                deals.append({
                    'deal_id': f"SAMPLE-DEAL-{i}",
                    'deal_name': f"Sample Deal {i + 1} - {'Product Sale' if i % 2 == 0 else 'Service Contract'}",
                    # FIXED
                    'lead_name': f"Sample Lead {i}",
                    'company': f"Company {i}",
                    'deal_value': random.randint(10000, 100000),
                    'deal_stage': random.choice(['Won', 'Negotiation', 'Proposal']),
                    'probability': random.randint(50, 95),
                    'expected_close_date': (datetime.now() + timedelta(days=random.randint(0, 60))).strftime(
                        '%Y-%m-%d'),
                    'created_date': datetime.now().strftime('%Y-%m-%d'),
                    'sales_rep': random.choice(['Alice Johnson', 'Bob Wilson', 'Carol Davis'])
                })

        deals_df = pd.DataFrame(deals)

        # Save to CSV
        deals_df.to_csv('sales_deals.csv', index=False)
        print(f"\n✅ Generated {len(deals_df)} sales deals")

        return deals_df

    def calculate_sales_metrics(self, deals_df):
        """Calculate key sales metrics"""
        # Convert close_date to datetime if it's not already
        deals_df['close_date'] = pd.to_datetime(deals_df['close_date'])

        # Won deals only
        won_deals = deals_df[deals_df['deal_stage'] == 'Won'].copy()

        if len(won_deals) == 0:
            return {
                'total_revenue': 0,
                'total_deals_won': 0,
                'total_deals_lost': 0,
                'win_rate': 0,
                'avg_deal_size': 0,
                'monthly_revenue': pd.DataFrame()
            }

        metrics = {
            'total_revenue': won_deals['deal_value'].sum(),
            'total_deals_won': len(won_deals),
            'total_deals_lost': len(deals_df[deals_df['deal_stage'] == 'Lost']),
            'win_rate': len(won_deals) / len(deals_df[deals_df['deal_stage'].isin(['Won', 'Lost'])]) * 100,
            'avg_deal_size': won_deals['deal_value'].mean(),
        }

        # Monthly revenue calculation
        won_deals['month'] = won_deals['close_date'].dt.to_period('M')
        monthly_revenue = won_deals.groupby('month').agg({
            'deal_value': ['sum', 'count'],
            'sales_rep': 'nunique'
        }).round(2)
        monthly_revenue.columns = ['Revenue', 'Deals_Count', 'Active_Reps']

        metrics['monthly_revenue'] = monthly_revenue

        return metrics

    def analyze_sales_funnel(self, leads_df):
        """Analyze the sales funnel conversion rates"""
        funnel_data = {
            'Stage': ['New', 'Contacted', 'Qualified', 'Converted', 'Lost'],
            'Count': [],
            'Conversion_Rate': []
        }

        total_leads = len(leads_df)
        if total_leads == 0:
            return pd.DataFrame(funnel_data)

        for stage in funnel_data['Stage']:
            count = len(leads_df[leads_df['status'] == stage])
            conversion_rate = (count / total_leads) * 100
            funnel_data['Count'].append(count)
            funnel_data['Conversion_Rate'].append(round(conversion_rate, 2))

        return pd.DataFrame(funnel_data)

    def prepare_forecast_features(self, deals_df):
        """Prepare features for revenue forecasting"""
        if len(deals_df) == 0:
            return pd.DataFrame()

        # Convert dates and create time-based features
        deals_df['close_date'] = pd.to_datetime(deals_df['close_date'])
        deals_df['month_num'] = deals_df['close_date'].dt.month
        deals_df['year'] = deals_df['close_date'].dt.year
        deals_df['quarter'] = deals_df['close_date'].dt.quarter

        # Create monthly aggregation for forecasting
        monthly_data = deals_df[deals_df['deal_stage'] == 'Won'].groupby(
            deals_df['close_date'].dt.to_period('M')
        ).agg({
            'deal_value': 'sum',
            'deal_id': 'count'
        }).reset_index()

        monthly_data.columns = ['month', 'revenue', 'deal_count']
        monthly_data['month_index'] = range(len(monthly_data))

        return monthly_data

    def train_forecast_model(self, deals_df):
        """Train revenue forecasting model"""
        try:
            monthly_data = self.prepare_forecast_features(deals_df)

            if len(monthly_data) < 3:
                print("Not enough historical data for forecasting. Need at least 3 months.")
                return False

            # Prepare features (X) and target (y)
            X = monthly_data[['month_index', 'deal_count']].values
            y = monthly_data['revenue'].values

            # Scale features
            X_scaled = self.scaler.fit_transform(X)

            # Train model
            self.forecast_model = LinearRegression()
            self.forecast_model.fit(X_scaled, y)

            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump({
                    'model': self.forecast_model,
                    'scaler': self.scaler,
                    'last_month_index': monthly_data['month_index'].max()
                }, f)

            self.is_trained = True
            print("Revenue forecasting model trained successfully!")
            return True

        except Exception as e:
            print(f"Error training forecast model: {e}")
            return False

    def forecast_revenue(self, deals_df, months_ahead=3):
        """Forecast future revenue"""
        if not self.is_trained:
            if not self.train_forecast_model(deals_df):
                # Fallback: simple projection based on average
                won_deals = deals_df[deals_df['deal_stage'] == 'Won']
                if len(won_deals) > 0:
                    avg_monthly_revenue = won_deals['deal_value'].sum() / 3  # Assume 3 months of data
                    forecasts = [avg_monthly_revenue * (1 + np.random.uniform(-0.1, 0.1)) for _ in range(months_ahead)]
                    return forecasts
                return [50000] * months_ahead  # Default forecast

        try:
            # Load model data
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                last_month_index = model_data['last_month_index']

            # Generate future features
            forecasts = []
            avg_deal_count = deals_df.groupby(pd.to_datetime(deals_df['close_date']).dt.to_period('M')).size().mean()

            for i in range(1, months_ahead + 1):
                future_month_index = last_month_index + i
                future_deal_count = max(1, int(avg_deal_count + np.random.normal(0, 1)))

                X_future = np.array([[future_month_index, future_deal_count]])
                X_future_scaled = self.scaler.transform(X_future)

                forecast = self.forecast_model.predict(X_future_scaled)[0]
                forecasts.append(max(0, forecast))  # Ensure non-negative

            return forecasts

        except Exception as e:
            print(f"Error forecasting revenue: {e}")
            return [50000] * months_ahead

    def create_sales_dashboard(self, deals_df, leads_df):
        """Create comprehensive sales dashboard"""
        print("\n=== SALES DASHBOARD ===")

        # Basic metrics
        metrics = self.calculate_sales_metrics(deals_df)

        print(f"Total Revenue: ${metrics['total_revenue']:,.2f}")
        print(f"Total Deals Won: {metrics['total_deals_won']}")
        print(f"Total Deals Lost: {metrics['total_deals_lost']}")
        print(f"Win Rate: {metrics['win_rate']:.2f}%")
        print(f"Average Deal Size: ${metrics['avg_deal_size']:,.2f}")

        # Monthly revenue
        if not metrics['monthly_revenue'].empty:
            print("\n--- MONTHLY REVENUE ---")
            print(metrics['monthly_revenue'])

        # Sales funnel
        print("\n--- SALES FUNNEL ---")
        funnel = self.analyze_sales_funnel(leads_df)
        print(funnel)

        # Revenue forecast
        print("\n--- REVENUE FORECAST (Next 3 Months) ---")
        forecasts = self.forecast_revenue(deals_df)
        for i, forecast in enumerate(forecasts, 1):
            print(f"Month {i}: ${forecast:,.2f}")

        return metrics, funnel, forecasts

    def visualize_sales_data(self, deals_df, leads_df):
        """Create sales visualizations"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))

            # 1. Revenue by Month
            won_deals = deals_df[deals_df['deal_stage'] == 'Won'].copy()
            if len(won_deals) > 0:
                won_deals['month'] = pd.to_datetime(won_deals['close_date']).dt.to_period('M')
                monthly_revenue = won_deals.groupby('month')['deal_value'].sum()

                axes[0, 0].bar(range(len(monthly_revenue)), monthly_revenue.values)
                axes[0, 0].set_title('Monthly Revenue')
                axes[0, 0].set_ylabel('Revenue ($)')
                axes[0, 0].set_xticks(range(len(monthly_revenue)))
                axes[0, 0].set_xticklabels([str(m) for m in monthly_revenue.index], rotation=45)

            # 2. Deal Stage Distribution
            stage_counts = deals_df['deal_stage'].value_counts()
            axes[0, 1].pie(stage_counts.values, labels=stage_counts.index, autopct='%1.1f%%')
            axes[0, 1].set_title('Deal Stage Distribution')

            # 3. Sales Funnel
            funnel = self.analyze_sales_funnel(leads_df)
            axes[1, 0].bar(funnel['Stage'], funnel['Count'])
            axes[1, 0].set_title('Sales Funnel')
            axes[1, 0].set_ylabel('Number of Leads')
            axes[1, 0].tick_params(axis='x', rotation=45)

            # 4. Revenue Forecast
            forecasts = self.forecast_revenue(deals_df)
            months = [f'Month {i}' for i in range(1, len(forecasts) + 1)]
            axes[1, 1].plot(months, forecasts, marker='o')
            axes[1, 1].set_title('Revenue Forecast')
            axes[1, 1].set_ylabel('Projected Revenue ($)')
            axes[1, 1].tick_params(axis='x', rotation=45)

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error creating visualizations: {e}")


# Demo function
def demo_sales_tracking():
    from lead_management import LeadManager

    # Load leads
    lm = LeadManager()
    leads = lm.leads_df

    if len(leads) == 0:
        print("No leads found. Please run lead_management.py first.")
        return

    # Initialize sales tracker
    tracker = SalesTracker()

    # Generate sales data
    deals = tracker.generate_sales_data(leads)

    # Create dashboard
    metrics, funnel, forecasts = tracker.create_sales_dashboard(deals, leads)

    # Create visualizations
    tracker.visualize
