from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from email_automation import EmailAutomation
from datetime import datetime

# ML Model Imports
from lead_management import LeadManager
from ai_lead_scoring import AILeadScorer
from churn_prediction import ChurnPredictor
from customer_segmentation import CustomerSegmentation
from sales_tracking import SalesTracker
from team_tracking import TeamTracker




import os

# Calculate correct paths since this file is in src/ folder
basedir = os.path.abspath(os.path.dirname(__file__))  # Gets src/ directory
project_root = os.path.dirname(basedir)  # Goes up one level to project root

app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# PostgreSQL Database (Production-ready)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_database.db'


# Or keep SQLite for local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (Update with your email credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'admin'  # UPDATE THIS
app.config['MAIL_PASSWORD'] = 'admin123'  # UPDATE THIS
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # UPDATE THIS

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
email_automation = EmailAutomation(mail)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    company = db.Column(db.String(120))
    status = db.Column(db.String(50), default='New')
    created_date = db.Column(db.String(50))
    last_contact = db.Column(db.String(50))
    notes = db.Column(db.Text)
    score = db.Column(db.Float, default=0)


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deal_name = db.Column(db.String(200), nullable=False)
    deal_value = db.Column(db.Float, nullable=False)
    deal_stage = db.Column(db.String(50), default='Prospecting')
    probability = db.Column(db.Integer, default=50)
    expected_close_date = db.Column(db.String(50))
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    created_date = db.Column(db.String(50))
    sales_rep = db.Column(db.String(120))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(100))
    assigned_to = db.Column(db.String(120))
    due_date = db.Column(db.String(50))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(50), default='Pending')
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))


# Create database tables
with app.app_context():
    db.create_all()

    # Create default admin user if doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@crm.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: username='admin', password='admin123'")


@login_manager.user_loader
def load_user(user_id):
    from sqlalchemy import select
    return db.session.get(User, int(user_id))


# Email Functions
def send_welcome_email(recipient_email, username):
    """Send welcome email to new users"""
    try:
        msg = Message(
            subject="Welcome to CRM Pro!",
            recipients=[recipient_email]
        )
        msg.body = f"""
Hello {username},

Welcome to CRM Pro! Your account has been successfully created.

You can now log in and start managing your leads, tracking sales, and analyzing performance.

Best regards,
The CRM Pro Team
        """
        mail.send(msg)
        print(f"Welcome email sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_lead_notification(lead_email, lead_name):
    """Send notification email for new leads"""
    try:
        msg = Message(
            subject="Thank you for your interest!",
            recipients=[lead_email]
        )
        msg.body = f"""
Hello {lead_name},

Thank you for your interest in our services. Our team will be in touch with you shortly.

Best regards,
The Sales Team
        """
        mail.send(msg)
        print(f"Lead notification sent to {lead_email}")
        return True
    except Exception as e:
        print(f"Error sending lead notification: {e}")
        return False


class ModernCRMDashboard:
    def __init__(self):
        self.app = app
        # Initialize ML Models
        self.lead_manager = LeadManager()
        self.lead_scorer = AILeadScorer()
        self.churn_predictor = ChurnPredictor()
        self.segmentation = CustomerSegmentation()
        self.sales_tracker = SalesTracker()
        self.team_tracker = TeamTracker()

        print("✅ All ML models loaded successfully!")

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if current_user.is_authenticated:
                return redirect(url_for('dashboard'))

            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')

                user = User.query.filter_by(username=username).first()

                if user and user.check_password(password):
                    login_user(user)
                    flash('Login successful!', 'success')
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password', 'error')

            return render_template('login.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if current_user.is_authenticated:
                return redirect(url_for('dashboard'))

            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')

                if password != confirm_password:
                    flash('Passwords do not match!', 'error')
                    return render_template('register.html')

                if User.query.filter_by(username=username).first():
                    flash('Username already exists!', 'error')
                    return render_template('register.html')

                if User.query.filter_by(email=email).first():
                    flash('Email already registered!', 'error')
                    return render_template('register.html')

                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                # Send welcome email to new user
                email_automation.send_welcome_email(new_user.email, new_user.username)

                # Send welcome email
                send_welcome_email(email, username)

                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))

            return render_template('register.html')

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            flash('You have been logged out.', 'info')
            return redirect(url_for('login'))

        @self.app.route('/')
        @login_required
        def dashboard():
            return render_template('dashboard.html', user=current_user)

        @self.app.route('/team')
        @login_required
        def team_dashboard():
            return render_template('team_dashboard.html', user=current_user)

        @self.app.route('/analytics')
        @login_required
        def analytics_dashboard():
            return render_template('analytics_dashboard.html', user=current_user)

        @self.app.route('/api/dashboard-data')
        @login_required
        def get_dashboard_data():
            return jsonify(self.get_sample_dashboard_data())

        @self.app.route('/api/team-data')
        @login_required
        def get_team_data():
            return jsonify(self.get_sample_team_data())

        @self.app.route('/api/analytics-data')
        @login_required
        def get_analytics_data():
            return jsonify(self.get_sample_analytics_data())

        @self.app.route('/api/leads', methods=['GET', 'POST'])
        @login_required
        def manage_leads():
            if request.method == 'POST':
                data = request.get_json()
                new_lead = Lead(
                    name=data.get('name'),
                    email=data.get('email'),
                    phone=data.get('phone'),
                    company=data.get('company'),
                    notes=data.get('notes', '')
                )
                db.session.add(new_lead)
                db.session.commit()

                # Send notification email to lead
                send_lead_notification(new_lead.email, new_lead.name)
                # Send notification email to lead
                email_automation.send_lead_notification(new_lead.email, new_lead.name)

                return jsonify({'success': True, 'message': 'Lead created successfully'})

            # GET request - return all leads
            leads = Lead.query.all()
            leads_data = [{
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'company': lead.company,
                'status': lead.status,
                'score': lead.score
            } for lead in leads]

            return jsonify(leads_data)

        @self.app.route('/api/send-followup/<int:lead_id>', methods=['POST'])
        @login_required
        def send_followup(lead_id):
            """Send follow-up email to a specific lead"""
            lead = Lead.query.get(lead_id)

            if not lead:
                return jsonify({'success': False, 'message': 'Lead not found'}), 404

            # Send follow-up email
            success = email_automation.send_followup_email(
                lead.email,
                lead.name,
                lead.last_contact if lead.last_contact else 'recently'
            )

            if success:
                return jsonify({'success': True, 'message': 'Follow-up email sent!'})
            else:
                return jsonify({'success': False, 'message': 'Failed to send email'}), 500

        @self.app.route('/api/send-retention/<int:customer_id>', methods=['POST'])
        @login_required
        def send_retention(customer_id):
            """Send retention email to at-risk customer"""
            # For demo, using Lead model - in production you'd have a Customer model
            customer = Lead.query.get(customer_id)

            if not customer:
                return jsonify({'success': False, 'message': 'Customer not found'}), 404

            # Send retention email
            success = email_automation.send_retention_email(
                customer.email,
                customer.name,
                customer.score if customer.score else 70  # Churn risk score
            )

            if success:
                return jsonify({'success': True, 'message': 'Retention email sent!'})
            else:
                return jsonify({'success': False, 'message': 'Failed to send email'}), 500

        @self.app.route('/api/export/<report_type>')
        @login_required
        def export_report(report_type):
            """Export reports as CSV"""
            try:
                if report_type == 'leads':
                    leads = self.lead_scorer.score_leads(self.lead_manager.leads_df)
                    leads.to_csv('export_leads.csv', index=False)
                    return jsonify({'success': True, 'file': 'export_leads.csv'})

                elif report_type == 'customers':
                    customers = self.churn_predictor.generate_customer_data(self.lead_manager.leads_df)
                    customers_risk = self.churn_predictor.predict_churn(customers)
                    customers_risk.to_csv('export_customers.csv', index=False)
                    return jsonify({'success': True, 'file': 'export_customers.csv'})

                elif report_type == 'team':
                    leads = self.lead_manager.leads_df
                    deals = self.sales_tracker.generate_sales_data(leads)
                    performance_df, _, _ = self.team_tracker.create_team_dashboard(leads, deals)
                    performance_df.to_csv('export_team_performance.csv', index=False)
                    return jsonify({'success': True, 'file': 'export_team_performance.csv'})

                else:
                    return jsonify({'success': False, 'message': 'Invalid report type'}), 400

            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500

        @self.app.route('/api/export/excel')
        @login_required
        def export_excel():
            """Export all data to Excel"""
            import pandas as pd
            from datetime import datetime

            # Create Excel writer
            filename = f"CRM_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Export leads
                leads = self.lead_manager.leads_df
                leads.to_excel(writer, sheet_name='Leads', index=False)

                # Export deals
                deals = self.sales_tracker.generate_sales_data(leads)
                deals.to_excel(writer, sheet_name='Deals', index=False)

                # Export team performance
                performance_df, _, _ = self.team_tracker.create_team_dashboard(leads, deals)
                performance_df.to_excel(writer, sheet_name='Team Performance', index=False)

            return jsonify({'success': True, 'file': filename})

    def get_sample_team_data(self):
        """Generate REAL team data from ML models"""
        try:
            leads = self.lead_manager.leads_df
            deals = self.sales_tracker.generate_sales_data(leads)

            # Use team tracker to get real performance
            performance_df, tasks_df, _ = self.team_tracker.create_team_dashboard(leads, deals)

            # Convert to JSON format
            team_performance = []
            for _, member in performance_df.iterrows():
                team_performance.append({
                    "name": member['team_member'],
                    "role": "Sales Rep",
                    "performance": float(member['performance_score']),
                    "revenue": float(member['total_revenue']),
                    "target": float(member['total_revenue'] * 1.2),
                    "deals_won": int(member['deals_won'])
                })

            # Team stats
            team_stats = {
                "total_members": len(performance_df),
                "avg_performance": float(performance_df['performance_score'].mean()),
                "total_revenue": float(performance_df['total_revenue'].sum()),
                "total_target": float(performance_df['total_revenue'].sum() * 1.2),
                "target_achievement": float(performance_df['performance_score'].mean())
            }

            # Recent tasks
            recent_tasks = []
            for _, task in tasks_df.head(3).iterrows():
                recent_tasks.append({
                    "assignee": task['assigned_to'],
                    "task": task['task_type'],
                    "priority": task['priority'],
                    "due": task['due_date']
                })

            return {
                "team_performance": team_performance,
                "team_stats": team_stats,
                "recent_tasks": recent_tasks
            }
        except Exception as e:
            print(f"Error getting team data: {e}")
            return self._get_fallback_team_data()

    def _get_fallback_team_data(self):
        """Fallback team data"""
        return {
            "team_performance": [
                {"name": "Team Member 1", "role": "Sales Rep", "performance": 85.0,
                 "revenue": 150000, "target": 180000, "deals_won": 5}
            ],
            "team_stats": {
                "total_members": 1,
                "avg_performance": 85.0,
                "total_revenue": 150000,
                "total_target": 180000,
                "target_achievement": 85.0
            },
            "recent_tasks": []
        }

    def get_sample_dashboard_data(self):
        """Generate REAL data from ML models for dashboard"""
        try:
            # Get real leads
            leads = self.lead_manager.leads_df

            # Score leads with AI
            scored_leads = self.lead_scorer.score_leads(leads)

            # Generate customer data and predict churn
            customers = self.churn_predictor.generate_customer_data(leads)
            customers_with_risk = self.churn_predictor.predict_churn(customers)

            # Generate sales data
            deals = self.sales_tracker.generate_sales_data(leads)

            # Calculate real KPIs
            total_revenue = deals[deals['deal_stage'] == 'Won']['deal_value'].sum()
            total_leads = len(leads)
            converted_leads = len(leads[leads['status'] == 'Converted'])
            conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
            high_risk_customers = len(customers_with_risk[customers_with_risk['churn_risk_score'] >= 70])
            churn_rate = (high_risk_customers / len(customers_with_risk) * 100) if len(customers_with_risk) > 0 else 0

            return {
                "kpis": {
                    "total_revenue": float(total_revenue),
                    "conversion_rate": round(conversion_rate, 2),
                    "churn_rate": round(churn_rate, 2),
                    "total_leads": int(total_leads),
                    "active_deals": len(deals[deals['deal_stage'].isin(['Negotiation', 'Proposal'])])
                },
                "revenue_trend": self._get_revenue_trend(deals),
                "pipeline_data": self._get_pipeline_data(leads),
                "recent_activities": self._get_recent_activities(leads, deals)
            }
        except Exception as e:
            print(f"Error getting dashboard data: {e}")
            # Return sample data if error
            return self._get_fallback_data()

    def _get_revenue_trend(self, deals):
        """Calculate monthly revenue trend"""
        import pandas as pd
        won_deals = deals[deals['deal_stage'] == 'Won'].copy()
        if len(won_deals) == 0:
            return [{"month": "Jan", "revenue": 0}]

        # Group by month (simplified)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue_by_month = []
        total = won_deals['deal_value'].sum()
        avg_per_month = total / 6

        for month in months:
            revenue_by_month.append({
                "month": month,
                "revenue": float(avg_per_month * (0.8 + 0.4 * (months.index(month) / 6)))
            })
        return revenue_by_month

    def _get_pipeline_data(self, leads):
        """Get lead pipeline distribution"""
        pipeline = leads['status'].value_counts()
        total = len(leads)

        pipeline_data = []
        for stage, count in pipeline.items():
            pipeline_data.append({
                "stage": stage,
                "count": int(count),
                "percentage": round((count / total * 100), 1)
            })
        return pipeline_data

    def _get_recent_activities(self, leads, deals):
        """Get recent lead and deal activities"""
        activities = []

        # Recent leads
        recent_leads = leads.sort_values('created_date', ascending=False).head(2)
        for _, lead in recent_leads.iterrows():
            activities.append({
                "type": "New Lead",
                "description": f"{lead['name']} from {lead['company']}",
                "amount": "",
                "time": "Today"
            })

        # Recent won deals
        won_deals = deals[deals['deal_stage'] == 'Won'].head(2)
        for _, deal in won_deals.iterrows():
            activities.append({
                "type": "Deal Won",
                "description": f"Deal closed - {deal['deal_name']}",
                "amount": f"${deal['deal_value']:,.0f}",
                "time": "Recently"
            })

        return activities[:4]  # Return max 4 activities

    def _get_fallback_data(self):
        """Fallback sample data if ML models fail"""
        return {
            "kpis": {
                "total_revenue": 2847350,
                "conversion_rate": 68.5,
                "churn_rate": 12.3,
                "total_leads": 1542,
                "active_deals": 89
            },
            "revenue_trend": [
                {"month": "Jan", "revenue": 245000},
                {"month": "Feb", "revenue": 289000},
                {"month": "Mar", "revenue": 324000},
                {"month": "Apr", "revenue": 298000},
                {"month": "May", "revenue": 367000},
                {"month": "Jun", "revenue": 389000}
            ],
            "pipeline_data": [
                {"stage": "New", "count": 342, "percentage": 22.2},
                {"stage": "Contacted", "count": 298, "percentage": 19.3},
                {"stage": "Qualified", "count": 256, "percentage": 16.6}
            ],
            "recent_activities": []
        }

    def get_sample_analytics_data(self):
        """Generate REAL analytics data"""
        try:
            leads = self.lead_manager.leads_df
            scored_leads = self.lead_scorer.score_leads(leads)
            customers = self.churn_predictor.generate_customer_data(leads)
            customers_with_risk = self.churn_predictor.predict_churn(customers)
            segmented = self.segmentation.segment_customers(customers)
            deals = self.sales_tracker.generate_sales_data(leads)

            # Real KPIs
            total_revenue = deals[deals['deal_stage'] == 'Won']['deal_value'].sum()
            conversion_rate = (len(leads[leads['status'] == 'Converted']) / len(leads) * 100)
            high_risk = len(customers_with_risk[customers_with_risk['churn_risk_score'] >= 70])
            churn_rate = (high_risk / len(customers_with_risk) * 100)

            # Growth calculation (simplified)
            growth_rate = 15.5  # You can calculate this from historical data

            return {
                "kpis": {
                    "total_revenue": float(total_revenue),
                    "conversion_rate": round(conversion_rate, 2),
                    "churn_rate": round(churn_rate, 2),
                    "growth_rate": growth_rate
                },
                "revenue_trend": self._get_revenue_trend(deals),
                "pipeline": self._get_pipeline_distribution(scored_leads),
                "segment_dist": segmented['segment_name'].value_counts().to_dict(),
                "churn_risk": [
                    len(customers_with_risk[customers_with_risk['churn_risk_score'] < 40]),
                    len(customers_with_risk[(customers_with_risk['churn_risk_score'] >= 40) &
                                            (customers_with_risk['churn_risk_score'] < 70)]),
                    len(customers_with_risk[customers_with_risk['churn_risk_score'] >= 70])
                ]
            }

        except Exception as e:
            print(f"Error getting analytics data: {e}")
            return self._get_fallback_analytics_data()

    def _get_revenue_trend(self, deals):
        """Calculate monthly revenue trend"""
        import pandas as pd
        from datetime import datetime

        won_deals = deals[deals['deal_stage'] == 'Won'].copy()

        if len(won_deals) == 0:
            # Return sample data if no deals
            return [
                {"month": "Jan", "revenue": 50000},
                {"month": "Feb", "revenue": 75000},
                {"month": "Mar", "revenue": 60000},
                {"month": "Apr", "revenue": 90000},
                {"month": "May", "revenue": 85000},
                {"month": "Jun", "revenue": 95000}
            ]

        # Calculate monthly totals
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue_by_month = []
        total = won_deals['deal_value'].sum()

        # Distribute revenue across months (simplified)
        for i, month in enumerate(months):
            base_revenue = total / 6
            variance = base_revenue * 0.3 * (i / len(months))
            revenue_by_month.append({
                "month": month,
                "revenue": float(base_revenue + variance)
            })

        return revenue_by_month

    def _get_pipeline_data(self, leads):
        """Get lead pipeline distribution"""
        if len(leads) == 0:
            return [{"stage": "No Data", "count": 0, "percentage": 0}]

        pipeline = leads['status'].value_counts()
        total = len(leads)

        pipeline_data = []
        for stage, count in pipeline.items():
            pipeline_data.append({
                "stage": stage,
                "count": int(count),
                "percentage": round((count / total * 100), 1)
            })

        return pipeline_data

    def _get_recent_activities(self, leads, deals):
        """Get recent lead and deal activities"""
        activities = []

        try:
            # Recent leads (sort by created_date if available)
            if 'created_date' in leads.columns and len(leads) > 0:
                recent_leads = leads.sort_values('created_date', ascending=False).head(2)
                for _, lead in recent_leads.iterrows():
                    activities.append({
                        "type": "New Lead",
                        "description": f"{lead['name']} from {lead['company']}",
                        "amount": "",
                        "time": "Recently"
                    })

            # Recent won deals
            if len(deals) > 0:
                won_deals = deals[deals['deal_stage'] == 'Won'].head(2)
                for _, deal in won_deals.iterrows():
                    activities.append({
                        "type": "Deal Won",
                        "description": f"{deal['deal_name']}",
                        "amount": f"${deal['deal_value']:,.0f}",
                        "time": "Recently"
                    })
        except Exception as e:
            print(f"Error getting activities: {e}")

        # Return sample if none found
        if len(activities) == 0:
            activities = [
                {"type": "New Lead", "description": "Sample Lead Activity", "amount": "", "time": "Today"},
                {"type": "Deal Won", "description": "Sample Deal Closed", "amount": "$50,000", "time": "Today"}
            ]

        return activities[:4]

    def _get_pipeline_distribution(self, scored_leads):
        """Get scored pipeline distribution"""
        if len(scored_leads) == 0:
            return [
                {"stage": "Hot (>70%)", "count": 0},
                {"stage": "Warm (40-70%)", "count": 0},
                {"stage": "Cold (<40%)", "count": 0}
            ]

        return [
            {"stage": "Hot (>70%)", "count": int(len(scored_leads[scored_leads['ai_score'] >= 70]))},
            {"stage": "Warm (40-70%)", "count": int(len(scored_leads[(scored_leads['ai_score'] >= 40) &
                                                                     (scored_leads['ai_score'] < 70)]))},
            {"stage": "Cold (<40%)", "count": int(len(scored_leads[scored_leads['ai_score'] < 40]))}
        ]

    def _get_pipeline_distribution(self, scored_leads):
        """Get scored pipeline distribution"""
        return [
            {"stage": "Hot (>70%)", "count": len(scored_leads[scored_leads['ai_score'] >= 70])},
            {"stage": "Warm (40-70%)", "count": len(scored_leads[(scored_leads['ai_score'] >= 40) &
                                                                 (scored_leads['ai_score'] < 70)])},
            {"stage": "Cold (<40%)", "count": len(scored_leads[scored_leads['ai_score'] < 40])}
        ]

    def _get_fallback_analytics_data(self):
        """Fallback analytics data"""
        return {
            "kpis": {"total_revenue": 2847350, "conversion_rate": 68.5,
                     "churn_rate": 12.3, "growth_rate": 22.1},
            "revenue_trend": [],
            "pipeline": [],
            "segment_dist": {},
            "churn_risk": [67, 45, 23]
        }

    def run(self, debug=True, port=5000):
        """Run the web dashboard"""
        print(f"\n🚀 Starting CRM Pro Dashboard...")
        print(f"📊 Dashboard: http://localhost:{port}/")
        print(f"🔐 Default Login: username='admin', password='admin123'")
        print(f"💡 Press Ctrl+C to stop the server\n")

        self.app.run(debug=debug, port=port, host='0.0.0.0')


# Demo function
def demo_web_dashboard():
    dashboard = ModernCRMDashboard()
    dashboard.run()


if __name__ == "__main__":
    demo_web_dashboard()
