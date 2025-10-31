from src.lead_management import LeadManager
from src.ai_lead_scoring import AILeadScorer
from src.churn_prediction import ChurnPredictor
from src.customer_segmentation import CustomerSegmentation


class CRMApplication:
    def __init__(self):
        self.lead_manager = LeadManager()
        self.lead_scorer = AILeadScorer()
        self.churn_predictor = ChurnPredictor()
        self.segmentation = CustomerSegmentation()

    def run_complete_demo(self):
        print("=== AI CRM SYSTEM DEMO ===\n")

        # 1. Lead Management
        print("1. CREATING SAMPLE LEADS...")
        self.lead_manager.create_lead("Alice Johnson", "alice@techstart.com", "555-0101", "TechStart Inc")
        self.lead_manager.create_lead("Bob Wilson", "bob@salesforce.com", "555-0102", "SalesCorp")
        self.lead_manager.create_lead("Carol Davis", "carol@marketing.com", "555-0103", "MarketPro")

        # Move some leads through pipeline
        self.lead_manager.move_lead_stage(1, "Contacted")
        self.lead_manager.move_lead_stage(1, "Qualified")
        self.lead_manager.move_lead_stage(1, "Converted")
        self.lead_manager.move_lead_stage(2, "Contacted")

        print("\n2. CURRENT LEADS:")
        self.lead_manager.read_leads()

        # 2. AI Lead Scoring
        print("\n3. AI LEAD SCORING...")
        scored_leads = self.lead_scorer.score_leads(self.lead_manager.leads_df)
        print(scored_leads[['name', 'company', 'status', 'ai_score', 'lead_category']].to_string(index=False))

        # 3. Churn Prediction
        print("\n4. CHURN PREDICTION...")
        customers = self.churn_predictor.generate_customer_data(self.lead_manager.leads_df)
        at_risk = self.churn_predictor.get_at_risk_customers(customers)

        # 4. Customer Segmentation
        print("\n5. CUSTOMER SEGMENTATION...")
        segmented = self.segmentation.segment_customers(customers)

        # Check if segmentation worked before analyzing
        if 'segment_name' in segmented.columns:
            print("\n--- CUSTOMER SEGMENTS ---")
            display_cols = ['name', 'monthly_spend', 'segment_name']
            available_cols = [col for col in display_cols if col in segmented.columns]
            if available_cols:
                print(segmented[available_cols].to_string(index=False))

            self.segmentation.analyze_segments(segmented)
        else:
            print("Segmentation failed - no segment_name column created")

        # 5. Sales Tracking & Forecasting
        print("\n6. SALES TRACKING & FORECASTING...")
        from src.sales_tracking import SalesTracker

        tracker = SalesTracker()
        deals = tracker.generate_sales_data(self.lead_manager.leads_df)
        metrics, funnel, forecasts = tracker.create_sales_dashboard(deals, self.lead_manager.leads_df)

        print("\n=== DEMO COMPLETED ===")

        # 6. Team Tracking & Performance
        print("\n7. TEAM TRACKING & PERFORMANCE...")
        from src.team_tracking import TeamTracker
        from src.sales_tracking import SalesTracker

        # Generate deals data for team analysis
        tracker = SalesTracker()
        deals = tracker.generate_sales_data(self.lead_manager.leads_df)

        # Team performance analysis
        team_tracker = TeamTracker()
        performance_df, tasks_df, recommendations_df = team_tracker.create_team_dashboard(self.lead_manager.leads_df,deals)

        # 8. Analytics Dashboard
        print("\n8. COMPREHENSIVE ANALYTICS DASHBOARD...")
        from src.analytics_dashboard import AnalyticsDashboard

        dashboard = AnalyticsDashboard()
        dashboard_metrics = dashboard.generate_full_dashboard(
            self.lead_manager.leads_df,
            customers,  # from churn prediction
            deals,  # from sales tracking
            performance_df,  # from team tracking
            segmented  # from customer segmentation
        )

        print("\n=== CRM ANALYTICS DASHBOARD COMPLETED ===")

        # 9. Launch Web Dashboard
        print("\n9. LAUNCHING MODERN WEB DASHBOARD...")
        print("🌐 Starting web server...")

        from src.web_dashboard import ModernCRMDashboard
        web_dashboard = ModernCRMDashboard()

        print("✅ CRM System Complete!")
        print("🚀 Web Dashboard available at: http://localhost:5000/")
        print("👥 Team Dashboard available at: http://localhost:5000/team")

        # Launch web dashboard
        web_dashboard.run()
def main():
    crm = CRMApplication()
    crm.run_complete_demo()


if __name__ == "__main__":
    main()
