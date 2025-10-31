import pandas as pd
import numpy as np
from datetime import datetime
import random


class GenAIOutreach:
    def __init__(self):
        # Email templates (simulating GenAI output)
        self.welcome_templates = [
            "Welcome to our platform, {name}! We're excited to have {company} on board.",
            "Hi {name}, thank you for joining us! Looking forward to helping {company} grow.",
            "Welcome {name}! Your journey with us at {company} starts now."
        ]

        self.followup_templates = [
            "Hi {name}, following up on our conversation about {company}'s needs.",
            "Hello {name}, I wanted to check if you had any questions about our solution for {company}.",
            "Hi {name}, hope you're doing well! Any updates on {company}'s decision?"
        ]

        self.retention_templates = [
            "Hi {name}, we noticed you haven't been active lately. How can we help {company}?",
            "Hello {name}, we miss you! Let's discuss how to better support {company}.",
            "Hi {name}, we'd love to re-engage with {company}. What can we improve?"
        ]

    def generate_welcome_email(self, lead_data):
        """Generate personalized welcome email for new users"""
        template = random.choice(self.welcome_templates)

        email_content = {
            'recipient': lead_data.get('email', ''),
            'subject': f"Welcome to our platform, {lead_data.get('name', '')}!",
            'body': template.format(
                name=lead_data.get('name', 'there'),
                company=lead_data.get('company', 'your company')
            ),
            'type': 'welcome',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return email_content

    def generate_followup_email(self, lead_data):
        """Generate follow-up email for leads"""
        template = random.choice(self.followup_templates)

        email_content = {
            'recipient': lead_data.get('email', ''),
            'subject': f"Following up with {lead_data.get('company', 'you')}",
            'body': template.format(
                name=lead_data.get('name', 'there'),
                company=lead_data.get('company', 'your company')
            ),
            'type': 'followup',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return email_content

    def generate_retention_email(self, customer_data):
        """Generate retention campaign email for at-risk customers"""
        template = random.choice(self.retention_templates)

        email_content = {
            'recipient': customer_data.get('email', ''),
            'subject': f"We miss you, {customer_data.get('name', '')}!",
            'body': template.format(
                name=customer_data.get('name', 'there'),
                company=customer_data.get('company', 'your company')
            ),
            'type': 'retention',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return email_content

    def bulk_generate_emails(self, leads_df, email_type='followup'):
        """Generate emails for multiple leads"""
        generated_emails = []

        for _, lead in leads_df.iterrows():
            lead_dict = lead.to_dict()

            if email_type == 'welcome':
                email = self.generate_welcome_email(lead_dict)
            elif email_type == 'followup':
                email = self.generate_followup_email(lead_dict)
            elif email_type == 'retention':
                email = self.generate_retention_email(lead_dict)
            else:
                continue

            generated_emails.append(email)

        return generated_emails

    def save_generated_emails(self, emails, filename='generated_emails.csv'):
        """Save generated emails to CSV"""
        emails_df = pd.DataFrame(emails)
        emails_df.to_csv(filename, index=False)
        print(f"Saved {len(emails)} generated emails to {filename}")

    def display_emails(self, emails, limit=3):
        """Display generated emails"""
        print("\n--- GENERATED EMAILS ---")
        for i, email in enumerate(emails[:limit]):
            print(f"\nEmail {i + 1}:")
            print(f"To: {email['recipient']}")
            print(f"Subject: {email['subject']}")
            print(f"Body: {email['body']}")
            print(f"Type: {email['type']}")
            print("-" * 50)


# Demo function
def demo_genai_outreach():
    from lead_management import LeadManager
    from churn_prediction import ChurnPredictor

    # Load leads
    lm = LeadManager()
    leads = lm.leads_df

    if len(leads) == 0:
        print("No leads found. Please run lead_management.py first.")
        return

    # Initialize outreach generator
    outreach = GenAIOutreach()

    # Generate welcome emails for new leads
    new_leads = leads[leads['status'] == 'New']
    if len(new_leads) > 0:
        welcome_emails = outreach.bulk_generate_emails(new_leads, 'welcome')
        print("WELCOME EMAILS:")
        outreach.display_emails(welcome_emails)

    # Generate follow-up emails for contacted leads
    contacted_leads = leads[leads['status'] == 'Contacted']
    if len(contacted_leads) > 0:
        followup_emails = outreach.bulk_generate_emails(contacted_leads, 'followup')
        print("\nFOLLOW-UP EMAILS:")
        outreach.display_emails(followup_emails)

    # Generate retention emails for at-risk customers
    predictor = ChurnPredictor()
    customers = predictor.generate_customer_data(leads)
    at_risk = customers.head(2)  # Take first 2 for demo

    if len(at_risk) > 0:
        retention_emails = outreach.bulk_generate_emails(at_risk, 'retention')
        print("\nRETENTION EMAILS:")
        outreach.display_emails(retention_emails)


if __name__ == "__main__":
    demo_genai_outreach()
