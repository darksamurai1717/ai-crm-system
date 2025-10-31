from flask_mail import Mail, Message
from datetime import datetime
import os


class EmailAutomation:
    """
    Automated Email System for CRM
    Handles welcome emails, follow-ups, retention campaigns, and notifications
    """

    def __init__(self, mail_instance):
        self.mail = mail_instance

    def send_welcome_email(self, recipient_email, username):
        """Send welcome email to new users"""
        try:
            msg = Message(
                subject="🎉 Welcome to CRM Pro!",
                recipients=[recipient_email]
            )
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #8b5cf6; margin: 0;">🚀 CRM Pro</h1>
                        </div>

                        <h2 style="color: #1a202c;">Welcome, {username}!</h2>

                        <p style="color: #64748b; line-height: 1.6;">
                            Thank you for joining CRM Pro! Your account has been successfully created.
                        </p>

                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <p style="color: white; margin: 0; font-weight: bold;">✨ What you can do now:</p>
                            <ul style="color: white; line-height: 1.8;">
                                <li>Manage your leads and track conversions</li>
                                <li>Monitor sales performance with AI insights</li>
                                <li>Analyze customer behavior and segments</li>
                                <li>Get automated recommendations for next-best actions</li>
                            </ul>
                        </div>

                        <p style="color: #64748b; line-height: 1.6;">
                            Ready to get started? Log in to your dashboard and explore the features!
                        </p>

                        <div style="text-align: center; margin-top: 30px;">
                            <a href="http://localhost:5000/login" 
                               style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 8px; 
                                      display: inline-block;
                                      font-weight: bold;">
                                Go to Dashboard
                            </a>
                        </div>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="color: #94a3b8; font-size: 14px; text-align: center;">
                            Need help? Contact us at support@crmPro.com<br>
                            © 2025 CRM Pro. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """

            self.mail.send(msg)
            print(f"✅ Welcome email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending welcome email: {e}")
            return False

    def send_lead_notification(self, lead_email, lead_name, company_name=""):
        """Send notification email to new leads"""
        try:
            msg = Message(
                subject="Thank you for your interest in CRM Pro!",
                recipients=[lead_email]
            )
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #1a202c;">Hello {lead_name}!</h2>

                        <p style="color: #64748b; line-height: 1.6;">
                            Thank you for your interest in CRM Pro. We received your inquiry and our sales team will be in touch with you shortly.
                        </p>

                        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #8b5cf6;">
                            <p style="margin: 0; color: #1a202c; font-weight: bold;">What happens next?</p>
                            <ul style="color: #64748b; line-height: 1.8; margin: 10px 0 0 0;">
                                <li>Our team will review your request within 24 hours</li>
                                <li>You'll receive a personalized demo invitation</li>
                                <li>We'll answer all your questions about our platform</li>
                            </ul>
                        </div>

                        <p style="color: #64748b; line-height: 1.6;">
                            In the meantime, feel free to explore our resources or reach out if you have any immediate questions.
                        </p>

                        <p style="color: #64748b; line-height: 1.6;">
                            Best regards,<br>
                            <strong style="color: #1a202c;">The CRM Pro Sales Team</strong>
                        </p>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="color: #94a3b8; font-size: 14px; text-align: center;">
                            © 2025 CRM Pro. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """

            self.mail.send(msg)
            print(f"✅ Lead notification sent to {lead_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending lead notification: {e}")
            return False

    def send_followup_email(self, recipient_email, recipient_name, last_contact_date):
        """Send follow-up email to leads"""
        try:
            msg = Message(
                subject=f"Following up on your CRM Pro inquiry",
                recipients=[recipient_email]
            )
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #1a202c;">Hi {recipient_name},</h2>

                        <p style="color: #64748b; line-height: 1.6;">
                            I wanted to follow up on our previous conversation about CRM Pro. I hope you've had a chance to think about how our platform could benefit your business.
                        </p>

                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <p style="color: white; margin: 0; font-weight: bold;">🎯 Quick Recap:</p>
                            <ul style="color: white; line-height: 1.8;">
                                <li>AI-powered lead scoring and prioritization</li>
                                <li>Automated customer churn prediction</li>
                                <li>Real-time sales analytics and forecasting</li>
                                <li>Intelligent task automation</li>
                            </ul>
                        </div>

                        <p style="color: #64748b; line-height: 1.6;">
                            Would you be available for a quick 15-minute call this week? I'd love to answer any questions you might have and show you how CRM Pro can specifically help your team.
                        </p>

                        <div style="text-align: center; margin: 30px 0;">
                            <a href="mailto:sales@crmpro.com" 
                               style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 8px; 
                                      display: inline-block;
                                      font-weight: bold;">
                                Schedule a Call
                            </a>
                        </div>

                        <p style="color: #64748b; line-height: 1.6;">
                            Looking forward to hearing from you!<br><br>
                            Best regards,<br>
                            <strong style="color: #1a202c;">Your Sales Team</strong>
                        </p>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="color: #94a3b8; font-size: 14px; text-align: center;">
                            © 2025 CRM Pro. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """

            self.mail.send(msg)
            print(f"✅ Follow-up email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending follow-up email: {e}")
            return False

    def send_retention_email(self, customer_email, customer_name, churn_risk_score):
        """Send retention campaign email for at-risk customers"""
        try:
            msg = Message(
                subject="We miss you! Let's reconnect 💙",
                recipients=[customer_email]
            )
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #1a202c;">We miss you, {customer_name}! 💙</h2>

                        <p style="color: #64748b; line-height: 1.6;">
                            We've noticed you haven't been active on CRM Pro lately, and we wanted to check in. Your success matters to us!
                        </p>

                        <div style="background: #fef3c7; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f59e0b;">
                            <p style="margin: 0; color: #92400e; font-weight: bold;">⚠️ We're here to help!</p>
                            <p style="color: #78350f; margin: 10px 0 0 0;">
                                If you're facing any challenges or have questions about using the platform, our support team is ready to assist you.
                            </p>
                        </div>

                        <h3 style="color: #1a202c;">What can we do for you?</h3>
                        <ul style="color: #64748b; line-height: 1.8;">
                            <li>📞 Schedule a free training session</li>
                            <li>💬 Get one-on-one support from our team</li>
                            <li>📊 Review your account setup and optimization</li>
                            <li>🎁 Explore new features you might have missed</li>
                        </ul>

                        <div style="text-align: center; margin: 30px 0;">
                            <a href="http://localhost:5000/login" 
                               style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 8px; 
                                      display: inline-block;
                                      font-weight: bold;">
                                Get Back to Your Dashboard
                            </a>
                        </div>

                        <p style="color: #64748b; line-height: 1.6;">
                            We're committed to your success. Let us know how we can make CRM Pro work better for you!
                        </p>

                        <p style="color: #64748b; line-height: 1.6;">
                            Warm regards,<br>
                            <strong style="color: #1a202c;">The CRM Pro Customer Success Team</strong>
                        </p>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="color: #94a3b8; font-size: 14px; text-align: center;">
                            Questions? Reply to this email or contact support@crmpro.com<br>
                            © 2025 CRM Pro. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """

            self.mail.send(msg)
            print(f"✅ Retention email sent to {customer_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending retention email: {e}")
            return False

    def send_task_reminder(self, user_email, user_name, task_description, due_date):
        """Send task reminder email"""
        try:
            msg = Message(
                subject="⏰ Task Reminder: Action Required",
                recipients=[user_email]
            )
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #1a202c;">Hi {user_name},</h2>

                        <p style="color: #64748b; line-height: 1.6;">
                            This is a friendly reminder about an upcoming task that requires your attention.
                        </p>

                        <div style="background: #fee2e2; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ef4444;">
                            <p style="margin: 0; color: #991b1b; font-weight: bold;">📋 Task Details:</p>
                            <p style="color: #7f1d1d; margin: 10px 0 5px 0;"><strong>Description:</strong> {task_description}</p>
                            <p style="color: #7f1d1d; margin: 5px 0 0 0;"><strong>Due Date:</strong> {due_date}</p>
                        </div>

                        <div style="text-align: center; margin: 30px 0;">
                            <a href="http://localhost:5000/" 
                               style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 8px; 
                                      display: inline-block;
                                      font-weight: bold;">
                                View Task in Dashboard
                            </a>
                        </div>

                        <p style="color: #94a3b8; font-size: 14px; text-align: center; margin-top: 30px;">
                            © 2025 CRM Pro. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """

            self.mail.send(msg)
            print(f"✅ Task reminder sent to {user_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending task reminder: {e}")
            return False


# Demo function for testing
def demo_email_system():
    """Test the email automation system"""
    from flask import Flask
    from flask_mail import Mail

    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # UPDATE THIS
    app.config['MAIL_PASSWORD'] = 'your-password'  # UPDATE THIS
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # UPDATE THIS

    mail = Mail(app)

    with app.app_context():
        email_system = EmailAutomation(mail)

        # Test welcome email
        email_system.send_welcome_email("test@example.com", "Test User")

        # Test lead notification
        email_system.send_lead_notification("lead@example.com", "John Doe", "Acme Corp")

        # Test follow-up email
        email_system.send_followup_email("followup@example.com", "Jane Smith", "2025-10-20")

        # Test retention email
        email_system.send_retention_email("retention@example.com", "Bob Johnson", 75.5)

        print("\n✅ All test emails sent!")


if __name__ == "__main__":
    demo_email_system()
