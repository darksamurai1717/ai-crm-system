import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random


class TeamTracker:
    def __init__(self):
        self.team_members = [
            {'id': 1, 'name': 'Alice Johnson', 'role': 'Sales Rep', 'hire_date': '2024-01-15',
             'target_monthly': 100000},
            {'id': 2, 'name': 'Bob Wilson', 'role': 'Sales Rep', 'hire_date': '2024-02-01', 'target_monthly': 95000},
            {'id': 3, 'name': 'Carol Davis', 'role': 'Senior Sales Rep', 'hire_date': '2023-08-10',
             'target_monthly': 120000},
            {'id': 4, 'name': 'David Brown', 'role': 'Sales Manager', 'hire_date': '2023-06-01',
             'target_monthly': 80000},
            {'id': 5, 'name': 'Eva Martinez', 'role': 'Sales Rep', 'hire_date': '2024-03-15', 'target_monthly': 90000}
        ]

        self.team_df = pd.DataFrame(self.team_members)

    def assign_leads_to_team(self, leads_df):
        """Assign leads to team members"""
        leads_with_reps = leads_df.copy()

        # Simple round-robin assignment
        team_names = self.team_df['name'].tolist()
        leads_with_reps['assigned_rep'] = [team_names[i % len(team_names)] for i in range(len(leads_df))]
        leads_with_reps['assigned_date'] = datetime.now().strftime('%Y-%m-%d')

        print(f"Assigned {len(leads_df)} leads to {len(team_names)} team members")
        return leads_with_reps

    def assign_deals_to_team(self, deals_df):
        """Assign deals to team members"""
        deals_with_reps = deals_df.copy()

        if 'sales_rep' not in deals_with_reps.columns:
            team_names = self.team_df['name'].tolist()
            deals_with_reps['sales_rep'] = [random.choice(team_names) for _ in range(len(deals_df))]

        return deals_with_reps

    def calculate_team_performance(self, leads_df, deals_df):
        """Calculate performance metrics for each team member"""
        # Assign leads and deals to team
        leads_assigned = self.assign_leads_to_team(leads_df)
        deals_assigned = self.assign_deals_to_team(deals_df)

        performance_data = []

        for _, member in self.team_df.iterrows():
            member_name = member['name']

            # Lead metrics
            member_leads = leads_assigned[leads_assigned['assigned_rep'] == member_name]
            total_leads = len(member_leads)
            converted_leads = len(member_leads[member_leads['status'] == 'Converted'])
            lead_conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0

            # Deal metrics
            member_deals = deals_assigned[deals_assigned['sales_rep'] == member_name]
            won_deals = member_deals[member_deals['deal_stage'] == 'Won']
            total_revenue = won_deals['deal_value'].sum() if len(won_deals) > 0 else 0
            deals_won = len(won_deals)
            deals_lost = len(member_deals[member_deals['deal_stage'] == 'Lost'])
            win_rate = (deals_won / (deals_won + deals_lost) * 100) if (deals_won + deals_lost) > 0 else 0

            # Calculate performance score (0-100)
            performance_score = (
                    (lead_conversion_rate * 0.3) +
                    (win_rate * 0.4) +
                    (min(total_revenue / member['target_monthly'], 1) * 100 * 0.3)
            )

            performance_data.append({
                'team_member': member_name,
                'role': member['role'],
                'total_leads': total_leads,
                'converted_leads': converted_leads,
                'lead_conversion_rate': round(lead_conversion_rate, 2),
                'deals_won': deals_won,
                'deals_lost': deals_lost,
                'win_rate': round(win_rate, 2),
                'total_revenue': round(total_revenue, 2),
                'target_monthly': member['target_monthly'],
                'target_achievement': round((total_revenue / member['target_monthly']) * 100, 2),
                'performance_score': round(performance_score, 2)
            })

        return pd.DataFrame(performance_data)

    def generate_team_tasks(self, leads_df, deals_df):
        """Generate tasks for team members"""
        tasks = []
        task_types = ['Follow-up call', 'Send proposal', 'Demo scheduling', 'Contract review', 'Client meeting']
        priorities = ['High', 'Medium', 'Low']

        # Assign leads and deals to get rep assignments
        leads_assigned = self.assign_leads_to_team(leads_df)
        deals_assigned = self.assign_deals_to_team(deals_df)

        # Generate tasks for each team member
        for _, member in self.team_df.iterrows():
            member_name = member['name']

            # Tasks from leads
            member_leads = leads_assigned[leads_assigned['assigned_rep'] == member_name]
            for _, lead in member_leads.head(3).iterrows():  # Limit to 3 per member
                tasks.append({
                    'task_id': len(tasks) + 1,
                    'assigned_to': member_name,
                    'task_type': random.choice(task_types),
                    'related_lead': lead['name'],
                    'related_company': lead['company'],
                    'priority': random.choice(priorities),
                    'due_date': (datetime.now() + timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d'),
                    'status': random.choice(['Pending', 'In Progress', 'Completed']),
                    'created_date': datetime.now().strftime('%Y-%m-%d')
                })

        return pd.DataFrame(tasks)

    def ai_workload_balancing(self, performance_df):
        """AI recommendations for workload balancing"""
        recommendations = []

        # Find overperforming and underperforming team members
        avg_performance = performance_df['performance_score'].mean()
        high_performers = performance_df[performance_df['performance_score'] > avg_performance + 10]
        low_performers = performance_df[performance_df['performance_score'] < avg_performance - 10]

        # Workload recommendations
        for _, performer in high_performers.iterrows():
            if performer['total_leads'] < performance_df['total_leads'].max():
                recommendations.append({
                    'team_member': performer['team_member'],
                    'recommendation_type': 'Increase Workload',
                    'suggestion': f"Assign more leads to {performer['team_member']} - currently high performing with {performer['performance_score']:.1f} score",
                    'priority': 'Medium'
                })

        for _, performer in low_performers.iterrows():
            recommendations.append({
                'team_member': performer['team_member'],
                'recommendation_type': 'Support & Training',
                'suggestion': f"Provide additional support to {performer['team_member']} - performance score is {performer['performance_score']:.1f}",
                'priority': 'High'
            })

        # Revenue target recommendations
        behind_target = performance_df[performance_df['target_achievement'] < 70]
        for _, member in behind_target.iterrows():
            recommendations.append({
                'team_member': member['team_member'],
                'recommendation_type': 'Revenue Focus',
                'suggestion': f"{member['team_member']} is at {member['target_achievement']:.1f}% of target - focus on high-value deals",
                'priority': 'High'
            })

        return pd.DataFrame(recommendations)

    def create_team_dashboard(self, leads_df, deals_df):
        """Create comprehensive team performance dashboard"""
        print("\n=== TEAM PERFORMANCE DASHBOARD ===")

        # Calculate performance metrics
        performance_df = self.calculate_team_performance(leads_df, deals_df)

        print("\n--- TEAM PERFORMANCE SUMMARY ---")
        display_cols = ['team_member', 'role', 'total_leads', 'lead_conversion_rate', 'deals_won', 'win_rate',
                        'total_revenue', 'target_achievement', 'performance_score']
        print(performance_df[display_cols].to_string(index=False))

        # Team tasks
        tasks_df = self.generate_team_tasks(leads_df, deals_df)
        print(f"\n--- ACTIVE TASKS ({len(tasks_df)} total) ---")
        task_summary = tasks_df.groupby(['assigned_to', 'status']).size().unstack(fill_value=0)
        print(task_summary)

        # AI workload recommendations
        recommendations_df = self.ai_workload_balancing(performance_df)
        print(f"\n--- AI WORKLOAD RECOMMENDATIONS ({len(recommendations_df)} suggestions) ---")
        if len(recommendations_df) > 0:
            for _, rec in recommendations_df.iterrows():
                print(f"• {rec['recommendation_type']} ({rec['priority']} Priority): {rec['suggestion']}")
        else:
            print("No specific workload balancing recommendations at this time.")

        # Team statistics
        print(f"\n--- TEAM STATISTICS ---")
        print(f"Total Team Members: {len(self.team_df)}")
        print(f"Average Performance Score: {performance_df['performance_score'].mean():.2f}")
        print(f"Total Team Revenue: ${performance_df['total_revenue'].sum():,.2f}")
        print(f"Team Win Rate: {performance_df['win_rate'].mean():.2f}%")
        print(f"Team Conversion Rate: {performance_df['lead_conversion_rate'].mean():.2f}%")

        return performance_df, tasks_df, recommendations_df

    def visualize_team_performance(self, performance_df):
        """Create team performance visualizations"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))

            # 1. Performance Score by Team Member
            axes[0, 0].bar(performance_df['team_member'], performance_df['performance_score'])
            axes[0, 0].set_title('Performance Score by Team Member')
            axes[0, 0].set_ylabel('Performance Score')
            axes[0, 0].tick_params(axis='x', rotation=45)

            # 2. Revenue vs Target
            x = range(len(performance_df))
            width = 0.35
            axes[0, 1].bar([i - width / 2 for i in x], performance_df['total_revenue'], width, label='Actual Revenue')
            axes[0, 1].bar([i + width / 2 for i in x], performance_df['target_monthly'], width, label='Target Revenue')
            axes[0, 1].set_title('Revenue vs Target by Team Member')
            axes[0, 1].set_ylabel('Revenue ($)')
            axes[0, 1].set_xticks(x)
            axes[0, 1].set_xticklabels(performance_df['team_member'], rotation=45)
            axes[0, 1].legend()

            # 3. Win Rate Distribution
            axes[1, 0].hist(performance_df['win_rate'], bins=5, edgecolor='black')
            axes[1, 0].set_title('Win Rate Distribution')
            axes[1, 0].set_xlabel('Win Rate (%)')
            axes[1, 0].set_ylabel('Number of Team Members')

            # 4. Lead Conversion Rate by Member
            axes[1, 1].bar(performance_df['team_member'], performance_df['lead_conversion_rate'])
            axes[1, 1].set_title('Lead Conversion Rate by Team Member')
            axes[1, 1].set_ylabel('Conversion Rate (%)')
            axes[1, 1].tick_params(axis='x', rotation=45)

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error creating team visualizations: {e}")

    def export_team_data(self, performance_df, tasks_df, recommendations_df):
        """Export team data to CSV files"""
        try:
            performance_df.to_csv('team_performance.csv', index=False)
            tasks_df.to_csv('team_tasks.csv', index=False)
            recommendations_df.to_csv('team_recommendations.csv', index=False)
            print("\nTeam data exported to CSV files:")
            print("- team_performance.csv")
            print("- team_tasks.csv")
            print("- team_recommendations.csv")
        except Exception as e:
            print(f"Error exporting team data: {e}")


# Demo function
def demo_team_tracking():
    from lead_management import LeadManager
    from sales_tracking import SalesTracker

    # Load leads and generate sales data
    lm = LeadManager()
    leads = lm.leads_df

    if len(leads) == 0:
        print("No leads found. Please run lead_management.py first.")
        return

    # Generate deals data
    tracker = SalesTracker()
    deals = tracker.generate_sales_data(leads)

    # Initialize team tracker
    team_tracker = TeamTracker()

    # Create team dashboard
    performance_df, tasks_df, recommendations_df = team_tracker.create_team_dashboard(leads, deals)

    # Create visualizations
    team_tracker.visualize_team_performance(performance_df)

    # Export data
    team_tracker.export_team_data(performance_df, tasks_df, recommendations_df)


if __name__ == "__main__":
    demo_team_tracking()
