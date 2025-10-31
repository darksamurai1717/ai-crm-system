import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class AnalyticsDashboard:
    def __init__(self):
        self.dashboard_data = {}
        self.kpi_targets = {
            'conversion_rate_target': 25.0,
            'churn_rate_target': 10.0,
            'win_rate_target': 60.0,
            'revenue_growth_target': 15.0
        }

    def collect_all_data(self, leads_df, customers_df, deals_df, performance_df, segmented_df):
        """Collect data from all CRM modules"""
        self.dashboard_data = {
            'leads': leads_df,
            'customers': customers_df,
            'deals': deals_df,
            'team_performance': performance_df,
            'customer_segments': segmented_df,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        print("Dashboard data collected successfully!")

    def calculate_key_metrics(self):
        """Calculate key business metrics for dashboard"""
        metrics = {}

        # Lead conversion metrics
        leads_df = self.dashboard_data.get('leads', pd.DataFrame())
        if not leads_df.empty:
            total_leads = len(leads_df)
            converted_leads = len(leads_df[leads_df['status'] == 'Converted'])
            metrics['total_leads'] = total_leads
            metrics['converted_leads'] = converted_leads
            metrics['conversion_rate'] = (converted_leads / total_leads * 100) if total_leads > 0 else 0

            # Lead pipeline distribution
            pipeline_dist = leads_df['status'].value_counts()
            metrics['pipeline_distribution'] = pipeline_dist.to_dict()
        else:
            metrics.update({
                'total_leads': 0, 'converted_leads': 0, 'conversion_rate': 0,
                'pipeline_distribution': {}
            })

        # Churn analysis
        customers_df = self.dashboard_data.get('customers', pd.DataFrame())
        if not customers_df.empty and 'churn_risk_score' in customers_df.columns:
            high_risk_customers = len(customers_df[customers_df['churn_risk_score'] >= 70])
            total_customers = len(customers_df)
            metrics['total_customers'] = total_customers
            metrics['high_risk_customers'] = high_risk_customers
            metrics['churn_percentage'] = (high_risk_customers / total_customers * 100) if total_customers > 0 else 0
            metrics['avg_churn_risk'] = customers_df['churn_risk_score'].mean()
        else:
            metrics.update({
                'total_customers': 0, 'high_risk_customers': 0,
                'churn_percentage': 0, 'avg_churn_risk': 0
            })

        # Sales metrics
        deals_df = self.dashboard_data.get('deals', pd.DataFrame())
        if not deals_df.empty:
            won_deals = deals_df[deals_df['deal_stage'] == 'Won']
            lost_deals = deals_df[deals_df['deal_stage'] == 'Lost']

            metrics['total_deals'] = len(deals_df)
            metrics['deals_won'] = len(won_deals)
            metrics['deals_lost'] = len(lost_deals)
            metrics['win_rate'] = (len(won_deals) / (len(won_deals) + len(lost_deals)) * 100) if (len(won_deals) + len(
                lost_deals)) > 0 else 0
            metrics['total_revenue'] = won_deals['deal_value'].sum() if len(won_deals) > 0 else 0
            metrics['avg_deal_size'] = won_deals['deal_value'].mean() if len(won_deals) > 0 else 0
        else:
            metrics.update({
                'total_deals': 0, 'deals_won': 0, 'deals_lost': 0,
                'win_rate': 0, 'total_revenue': 0, 'avg_deal_size': 0
            })

        # Team performance metrics
        performance_df = self.dashboard_data.get('team_performance', pd.DataFrame())
        if not performance_df.empty:
            metrics['team_size'] = len(performance_df)
            metrics['avg_team_performance'] = performance_df['performance_score'].mean()
            metrics['top_performer'] = performance_df.loc[performance_df['performance_score'].idxmax(), 'team_member']
            metrics['team_total_revenue'] = performance_df['total_revenue'].sum()
        else:
            metrics.update({
                'team_size': 0, 'avg_team_performance': 0,
                'top_performer': 'N/A', 'team_total_revenue': 0
            })

        # Customer segmentation metrics
        segmented_df = self.dashboard_data.get('customer_segments', pd.DataFrame())
        if not segmented_df.empty and 'segment_name' in segmented_df.columns:
            segment_dist = segmented_df['segment_name'].value_counts()
            metrics['segment_distribution'] = segment_dist.to_dict()

            if 'monthly_spend' in segmented_df.columns:
                metrics['avg_customer_value'] = segmented_df['monthly_spend'].mean()
            else:
                metrics['avg_customer_value'] = 0
        else:
            metrics.update({
                'segment_distribution': {}, 'avg_customer_value': 0
            })

        return metrics

    def create_executive_summary(self, metrics):
        """Create executive summary with key insights"""
        print("\n" + "=" * 60)
        print("         EXECUTIVE DASHBOARD SUMMARY")
        print("=" * 60)

        # Key Performance Indicators
        print("\n📊 KEY PERFORMANCE INDICATORS")
        print("-" * 40)
        print(f"💰 Total Revenue:           ${metrics['total_revenue']:,.2f}")
        print(f"👥 Total Customers:         {metrics['total_customers']}")
        print(f"📈 Lead Conversion Rate:    {metrics['conversion_rate']:.2f}%")
        print(f"🎯 Sales Win Rate:          {metrics['win_rate']:.2f}%")
        print(f"⚠️  Customer Churn Risk:     {metrics['churn_percentage']:.2f}%")

        # Performance vs Targets
        print(f"\n🎯 PERFORMANCE VS TARGETS")
        print("-" * 40)
        conversion_status = "✅ Above" if metrics['conversion_rate'] >= self.kpi_targets[
            'conversion_rate_target'] else "❌ Below"
        churn_status = "✅ Below" if metrics['churn_percentage'] <= self.kpi_targets['churn_rate_target'] else "❌ Above"
        win_rate_status = "✅ Above" if metrics['win_rate'] >= self.kpi_targets['win_rate_target'] else "❌ Below"

        print(f"Conversion Rate: {conversion_status} Target ({self.kpi_targets['conversion_rate_target']}%)")
        print(f"Churn Rate:      {churn_status} Target ({self.kpi_targets['churn_rate_target']}%)")
        print(f"Win Rate:        {win_rate_status} Target ({self.kpi_targets['win_rate_target']}%)")

        # Team Performance
        print(f"\n👥 TEAM PERFORMANCE")
        print("-" * 40)
        print(f"Team Size:                  {metrics['team_size']} members")
        print(f"Average Performance Score:  {metrics['avg_team_performance']:.2f}/100")
        print(f"Top Performer:              {metrics['top_performer']}")
        print(f"Team Total Revenue:         ${metrics['team_total_revenue']:,.2f}")

        # Business Insights
        print(f"\n💡 KEY INSIGHTS")
        print("-" * 40)

        insights = []
        if metrics['conversion_rate'] < self.kpi_targets['conversion_rate_target']:
            insights.append(
                f"• Conversion rate ({metrics['conversion_rate']:.1f}%) below target - focus on lead quality")
        if metrics['churn_percentage'] > self.kpi_targets['churn_rate_target']:
            insights.append(f"• High churn risk ({metrics['churn_percentage']:.1f}%) - implement retention campaigns")
        if metrics['win_rate'] > self.kpi_targets['win_rate_target']:
            insights.append(f"• Excellent win rate ({metrics['win_rate']:.1f}%) - sales process is effective")
        if metrics['avg_deal_size'] > 0:
            insights.append(f"• Average deal size: ${metrics['avg_deal_size']:,.2f}")

        if not insights:
            insights.append("• All key metrics are performing well!")

        for insight in insights:
            print(insight)

    def create_detailed_analytics(self, metrics):
        """Create detailed analytics breakdown"""
        print(f"\n📊 DETAILED ANALYTICS BREAKDOWN")
        print("=" * 50)

        # Sales Pipeline Analysis
        if metrics['pipeline_distribution']:
            print(f"\n🔄 SALES PIPELINE BREAKDOWN")
            print("-" * 30)
            total_pipeline = sum(metrics['pipeline_distribution'].values())
            for stage, count in metrics['pipeline_distribution'].items():
                percentage = (count / total_pipeline * 100) if total_pipeline > 0 else 0
                print(f"{stage:<12}: {count:>3} leads ({percentage:>5.1f}%)")

        # Customer Segmentation Analysis
        if metrics['segment_distribution']:
            print(f"\n👥 CUSTOMER SEGMENTATION")
            print("-" * 30)
            total_segments = sum(metrics['segment_distribution'].values())
            for segment, count in metrics['segment_distribution'].items():
                percentage = (count / total_segments * 100) if total_segments > 0 else 0
                print(f"{segment:<15}: {count:>3} customers ({percentage:>5.1f}%)")

        # Revenue Analysis
        print(f"\n💰 REVENUE ANALYSIS")
        print("-" * 30)
        print(f"Total Revenue:      ${metrics['total_revenue']:>12,.2f}")
        print(f"Average Deal Size:  ${metrics['avg_deal_size']:>12,.2f}")
        print(f"Revenue per Customer: ${metrics['total_revenue'] / max(1, metrics['total_customers']):>10,.2f}")

        # Risk Analysis
        print(f"\n⚠️  RISK ANALYSIS")
        print("-" * 30)
        print(f"High Risk Customers: {metrics['high_risk_customers']:>8}")
        print(f"Average Churn Risk:  {metrics['avg_churn_risk']:>11.2f}%")
        print(f"Customer Health:     {'Good' if metrics['churn_percentage'] < 15 else 'Concerning':>8}")

    def create_comprehensive_visualizations(self, metrics):
        """Create comprehensive dashboard visualizations"""
        try:
            fig = plt.figure(figsize=(20, 16))

            # Create a 3x3 grid of subplots
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

            # 1. KPI Gauge Chart (simulated)
            ax1 = fig.add_subplot(gs[0, 0])
            kpis = ['Conversion Rate', 'Win Rate', 'Churn Rate']
            values = [metrics['conversion_rate'], metrics['win_rate'], metrics['churn_percentage']]
            targets = [self.kpi_targets['conversion_rate_target'],
                       self.kpi_targets['win_rate_target'],
                       self.kpi_targets['churn_rate_target']]

            x = np.arange(len(kpis))
            width = 0.35
            ax1.bar(x - width / 2, values, width, label='Actual', alpha=0.8)
            ax1.bar(x + width / 2, targets, width, label='Target', alpha=0.6)
            ax1.set_xlabel('KPIs')
            ax1.set_ylabel('Percentage')
            ax1.set_title('KPI Performance vs Targets')
            ax1.set_xticks(x)
            ax1.set_xticklabels(kpis, rotation=45)
            ax1.legend()

            # 2. Revenue Trend (simulated monthly data)
            ax2 = fig.add_subplot(gs[0, 1])
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            revenue_trend = np.random.normal(metrics['total_revenue'] / 6, metrics['total_revenue'] / 20, 6)
            revenue_trend = np.abs(revenue_trend)  # Ensure positive
            ax2.plot(months, revenue_trend, marker='o', linewidth=2, markersize=8)
            ax2.set_title('Monthly Revenue Trend')
            ax2.set_ylabel('Revenue ($)')
            ax2.grid(True, alpha=0.3)

            # 3. Sales Pipeline
            ax3 = fig.add_subplot(gs[0, 2])
            if metrics['pipeline_distribution']:
                pipeline_labels = list(metrics['pipeline_distribution'].keys())
                pipeline_values = list(metrics['pipeline_distribution'].values())
                colors = plt.cm.Set3(np.linspace(0, 1, len(pipeline_labels)))
                ax3.pie(pipeline_values, labels=pipeline_labels, autopct='%1.1f%%', colors=colors)
                ax3.set_title('Sales Pipeline Distribution')

            # 4. Customer Segmentation
            ax4 = fig.add_subplot(gs[1, 0])
            if metrics['segment_distribution']:
                segment_labels = list(metrics['segment_distribution'].keys())
                segment_values = list(metrics['segment_distribution'].values())
                ax4.bar(segment_labels, segment_values, color='skyblue')
                ax4.set_title('Customer Segments')
                ax4.set_ylabel('Number of Customers')
                ax4.tick_params(axis='x', rotation=45)

            # 5. Team Performance (if available)
            ax5 = fig.add_subplot(gs[1, 1])
            performance_df = self.dashboard_data.get('team_performance', pd.DataFrame())
            if not performance_df.empty and len(performance_df) > 0:
                team_members = performance_df['team_member'].head(5)  # Show top 5
                performance_scores = performance_df['performance_score'].head(5)
                ax5.barh(team_members, performance_scores, color='lightgreen')
                ax5.set_title('Team Performance Scores')
                ax5.set_xlabel('Performance Score')
            else:
                ax5.text(0.5, 0.5, 'No Team Data', ha='center', va='center', transform=ax5.transAxes)
                ax5.set_title('Team Performance')

            # 6. Churn Risk Distribution
            ax6 = fig.add_subplot(gs[1, 2])
            customers_df = self.dashboard_data.get('customers', pd.DataFrame())
            if not customers_df.empty and 'churn_risk_score' in customers_df.columns:
                ax6.hist(customers_df['churn_risk_score'], bins=10, color='coral', alpha=0.7, edgecolor='black')
                ax6.axvline(x=70, color='red', linestyle='--', label='High Risk Threshold')
                ax6.set_title('Customer Churn Risk Distribution')
                ax6.set_xlabel('Churn Risk Score')
                ax6.set_ylabel('Number of Customers')
                ax6.legend()
            else:
                ax6.text(0.5, 0.5, 'No Churn Data', ha='center', va='center', transform=ax6.transAxes)
                ax6.set_title('Churn Risk Distribution')

            # 7. Deal Value Distribution
            ax7 = fig.add_subplot(gs[2, 0])
            deals_df = self.dashboard_data.get('deals', pd.DataFrame())
            if not deals_df.empty and 'deal_value' in deals_df.columns:
                won_deals = deals_df[deals_df['deal_stage'] == 'Won']
                if len(won_deals) > 0:
                    ax7.hist(won_deals['deal_value'], bins=8, color='gold', alpha=0.7, edgecolor='black')
                    ax7.set_title('Won Deal Value Distribution')
                    ax7.set_xlabel('Deal Value ($)')
                    ax7.set_ylabel('Number of Deals')

            # 8. Lead Scoring Distribution (if available)
            ax8 = fig.add_subplot(gs[2, 1])
            leads_df = self.dashboard_data.get('leads', pd.DataFrame())
            if not leads_df.empty and 'ai_score' in leads_df.columns:
                ax8.hist(leads_df['ai_score'], bins=10, color='lightblue', alpha=0.7, edgecolor='black')
                ax8.set_title('Lead Score Distribution')
                ax8.set_xlabel('AI Lead Score')
                ax8.set_ylabel('Number of Leads')
            else:
                ax8.text(0.5, 0.5, 'No Lead Scores', ha='center', va='center', transform=ax8.transAxes)
                ax8.set_title('Lead Score Distribution')

            # 9. Business Health Indicator
            ax9 = fig.add_subplot(gs[2, 2])
            health_metrics = ['Revenue', 'Conversion', 'Win Rate', 'Low Churn']
            health_scores = [
                min(100, (metrics['total_revenue'] / 100000) * 100),  # Scale revenue
                metrics['conversion_rate'],
                metrics['win_rate'],
                100 - metrics['churn_percentage']  # Invert churn for health
            ]

            angles = np.linspace(0, 2 * np.pi, len(health_metrics), endpoint=False).tolist()
            health_scores += health_scores[:1]  # Complete the circle
            angles += angles[:1]

            ax9 = plt.subplot(gs[2, 2], projection='polar')
            ax9.plot(angles, health_scores, 'o-', linewidth=2, color='green')
            ax9.fill(angles, health_scores, alpha=0.25, color='green')
            ax9.set_xticks(angles[:-1])
            ax9.set_xticklabels(health_metrics)
            ax9.set_ylim(0, 100)
            ax9.set_title('Business Health Radar', pad=20)

            plt.suptitle('CRM Analytics Dashboard', fontsize=16, y=0.98)
            plt.show()

        except Exception as e:
            print(f"Error creating comprehensive visualizations: {e}")
            print("Showing simplified charts instead...")
            self.create_simple_charts(metrics)

    def create_simple_charts(self, metrics):
        """Create simple fallback charts"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))

            # Simple KPI bars
            kpis = ['Conversion Rate', 'Win Rate', 'Churn Rate']
            values = [metrics['conversion_rate'], metrics['win_rate'], metrics['churn_percentage']]
            axes[0, 0].bar(kpis, values)
            axes[0, 0].set_title('Key Performance Indicators')
            axes[0, 0].set_ylabel('Percentage')

            # Revenue summary
            revenue_data = ['Total Revenue', 'Avg Deal Size']
            revenue_values = [metrics['total_revenue'], metrics['avg_deal_size']]
            axes[0, 1].bar(revenue_data, revenue_values)
            axes[0, 1].set_title('Revenue Metrics')
            axes[0, 1].set_ylabel('Value ($)')

            # Team metrics
            team_data = ['Team Size', 'Avg Performance']
            team_values = [metrics['team_size'], metrics['avg_team_performance']]
            axes[1, 0].bar(team_data, team_values)
            axes[1, 0].set_title('Team Metrics')

            # Customer metrics
            customer_data = ['Total Customers', 'High Risk']
            customer_values = [metrics['total_customers'], metrics['high_risk_customers']]
            axes[1, 1].bar(customer_data, customer_values)
            axes[1, 1].set_title('Customer Metrics')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error creating simple charts: {e}")

    def export_dashboard_data(self, metrics):
        """Export dashboard data for reporting"""
        try:
            # Create dashboard summary
            dashboard_summary = pd.DataFrame([{
                'metric': k,
                'value': v,
                'last_updated': self.dashboard_data['last_updated']
            } for k, v in metrics.items() if not isinstance(v, dict)])

            dashboard_summary.to_csv('dashboard_summary.csv', index=False)

            # Export KPI report
            kpi_report = pd.DataFrame([
                {'KPI': 'Lead Conversion Rate', 'Actual': metrics['conversion_rate'],
                 'Target': self.kpi_targets['conversion_rate_target'],
                 'Status': 'Above Target' if metrics['conversion_rate'] >= self.kpi_targets[
                     'conversion_rate_target'] else 'Below Target'},
                {'KPI': 'Sales Win Rate', 'Actual': metrics['win_rate'], 'Target': self.kpi_targets['win_rate_target'],
                 'Status': 'Above Target' if metrics['win_rate'] >= self.kpi_targets[
                     'win_rate_target'] else 'Below Target'},
                {'KPI': 'Customer Churn Rate', 'Actual': metrics['churn_percentage'],
                 'Target': self.kpi_targets['churn_rate_target'],
                 'Status': 'Below Target' if metrics['churn_percentage'] <= self.kpi_targets[
                     'churn_rate_target'] else 'Above Target'}
            ])

            kpi_report.to_csv('kpi_report.csv', index=False)

            print("\nDashboard data exported:")
            print("- dashboard_summary.csv")
            print("- kpi_report.csv")

        except Exception as e:
            print(f"Error exporting dashboard data: {e}")

    def generate_full_dashboard(self, leads_df, customers_df, deals_df, performance_df, segmented_df):
        """Generate complete analytics dashboard"""
        # Collect all data
        self.collect_all_data(leads_df, customers_df, deals_df, performance_df, segmented_df)

        # Calculate metrics
        metrics = self.calculate_key_metrics()

        # Create executive summary
        self.create_executive_summary(metrics)

        # Create detailed analytics
        self.create_detailed_analytics(metrics)

        # Create visualizations
        self.create_comprehensive_visualizations(metrics)

        # Export data
        self.export_dashboard_data(metrics)

        return metrics


# Demo function
def demo_analytics_dashboard():
    from lead_management import LeadManager
    from churn_prediction import ChurnPredictor
    from sales_tracking import SalesTracker
    from team_tracking import TeamTracker
    from customer_segmentation import CustomerSegmentation

    print("Loading all CRM data for analytics dashboard...")

    # Load all data
    lm = LeadManager()
    leads = lm.leads_df

    if len(leads) == 0:
        print("No leads found. Please run other modules first.")
        return

    # Generate all required data
    predictor = ChurnPredictor()
    customers = predictor.generate_customer_data(leads)
    customers_with_risk = predictor.predict_churn(customers)

    tracker = SalesTracker()
    deals = tracker.generate_sales_data(leads)

    team_tracker = TeamTracker()
    performance_df, _, _ = team_tracker.create_team_dashboard(leads, deals)

    segmentation = CustomerSegmentation()
    segmented = segmentation.segment_customers(customers)

    # Generate dashboard
    dashboard = AnalyticsDashboard()
    metrics = dashboard.generate_full_dashboard(leads, customers_with_risk, deals, performance_df, segmented)

    print(f"\n🎉 Analytics Dashboard Generated Successfully!")
    print(f"Last Updated: {dashboard.dashboard_data['last_updated']}")


if __name__ == "__main__":
    demo_analytics_dashboard()
