import pandas as pd
import json
from datetime import datetime
import os


class LeadManager:
    def __init__(self, csv_file='leads.csv'):
        """Initialize Lead Manager and load existing leads"""
        self.csv_file = csv_file

        # Create leads file if doesn't exist
        if not os.path.exists(self.csv_file):
            print(f"Creating new leads database: {self.csv_file}")
            self.leads_df = pd.DataFrame(columns=['name', 'email', 'phone', 'company', 'status',
                                                  'created_date', 'last_contact', 'notes', 'score'])
            # Add sample leads
            self._create_sample_leads()
            self.save_leads()
        else:
            self.leads_df = pd.read_csv(self.csv_file)
            print(f"✅ Loaded {len(self.leads_df)} leads from {self.csv_file}")

        # If still empty, add sample leads
        if len(self.leads_df) == 0:
            self._create_sample_leads()
            self.save_leads()

    def save_leads(self):
        """Save leads database to file."""
        self.leads_df.to_csv(self.csv_file, index=False)
        print(f"✅ Leads saved to {self.csv_file}")

    def _create_sample_leads(self):
        """Create sample leads for testing"""
        from datetime import datetime, timedelta
        import random

        sample_leads = [
            {
                'name': 'John Smith',
                'email': 'john.smith@techcorp.com',
                'phone': '555-0101',
                'company': 'TechCorp Inc',
                'status': 'New',
                'created_date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                'last_contact': datetime.now().strftime('%Y-%m-%d'),
                'notes': 'Interested in enterprise plan',
                'score': 0
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.j@innovate.com',
                'phone': '555-0102',
                'company': 'Innovate Solutions',
                'status': 'Contacted',
                'created_date': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'notes': 'Demo scheduled for next week',
                'score': 0
            },
            {
                'name': 'Mike Davis',
                'email': 'mike.davis@startupco.com',
                'phone': '555-0103',
                'company': 'StartupCo',
                'status': 'Qualified',
                'created_date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'notes': 'Budget approved, awaiting final decision',
                'score': 0
            },
            {
                'name': 'Emily Brown',
                'email': 'emily.b@globaltech.com',
                'phone': '555-0104',
                'company': 'GlobalTech',
                'status': 'Converted',
                'created_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                'notes': 'Signed annual contract - $50K',
                'score': 0
            },
            {
                'name': 'Robert Wilson',
                'email': 'r.wilson@marketingpro.com',
                'phone': '555-0105',
                'company': 'Marketing Pro',
                'status': 'New',
                'created_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                'notes': 'Requested pricing information',
                'score': 0
            },
            {
                'name': 'Lisa Anderson',
                'email': 'l.anderson@salesforce99.com',
                'phone': '555-0106',
                'company': 'SalesForce 99',
                'status': 'Contacted',
                'created_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'last_contact': datetime.now().strftime('%Y-%m-%d'),
                'notes': 'Follow-up call scheduled',
                'score': 0
            },
            {
                'name': 'David Martinez',
                'email': 'd.martinez@consulting.com',
                'phone': '555-0107',
                'company': 'Consulting Group',
                'status': 'Qualified',
                'created_date': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'notes': 'Interested in premium features',
                'score': 0
            },
            {
                'name': 'Jennifer Lee',
                'email': 'j.lee@dataanalytics.com',
                'phone': '555-0108',
                'company': 'Data Analytics Co',
                'status': 'New',
                'created_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'notes': 'Website inquiry - needs demo',
                'score': 0
            }
        ]

        self.leads_df = pd.DataFrame(sample_leads)
        print(f"✅ Created {len(self.leads_df)} sample leads")

    def load_data(self):
        """Load leads data from CSV file"""
        try:
            if os.path.exists(self.data_file):
                return pd.read_csv(self.data_file)
            else:
                # Create empty DataFrame with required columns
                columns = ['id', 'name', 'email', 'phone', 'company', 'status',
                           'created_date', 'last_contact', 'notes', 'score']
                return pd.DataFrame(columns=columns)
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

    def create_lead(self, name, email, phone, company, notes=""):
        """Create a new lead"""
        new_id = len(self.leads_df) + 1
        new_lead = {
            'id': new_id,
            'name': name,
            'email': email,
            'phone': phone,
            'company': company,
            'status': 'New',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_contact': '',
            'notes': notes,
            'score': 0
        }

        self.leads_df = pd.concat([self.leads_df, pd.DataFrame([new_lead])],
                                  ignore_index=True)
        self.save_data()
        print(f"Lead created successfully: {name}")
        return new_id

    def read_leads(self, status=None):
        """Read/Display leads"""
        if status:
            filtered_leads = self.leads_df[self.leads_df['status'] == status]
        else:
            filtered_leads = self.leads_df

        print("\n--- LEADS ---")
        print(filtered_leads.to_string(index=False))
        return filtered_leads

    def update_lead(self, lead_id, **kwargs):
        """Update lead information"""
        if lead_id in self.leads_df['id'].values:
            for key, value in kwargs.items():
                if key in self.leads_df.columns:
                    self.leads_df.loc[self.leads_df['id'] == lead_id, key] = value

            self.leads_df.loc[self.leads_df['id'] == lead_id, 'last_contact'] = \
                datetime.now().strftime('%Y-%m-%d')
            self.save_data()
            print(f"Lead {lead_id} updated successfully")
        else:
            print(f"Lead with ID {lead_id} not found")

    def delete_lead(self, lead_id):
        """Delete a lead"""
        if lead_id in self.leads_df['id'].values:
            self.leads_df = self.leads_df[self.leads_df['id'] != lead_id]
            self.save_data()
            print(f"Lead {lead_id} deleted successfully")
        else:
            print(f"Lead with ID {lead_id} not found")

    def move_lead_stage(self, lead_id, new_status):
        """Move lead through pipeline stages"""
        valid_statuses = ['New', 'Contacted', 'Qualified', 'Converted', 'Lost']
        if new_status in valid_statuses:
            self.update_lead(lead_id, status=new_status)
            print(f"Lead {lead_id} moved to {new_status}")
        else:
            print(f"Invalid status. Use: {valid_statuses}")

    def import_from_csv(self, file_path):
        """Import leads from CSV file"""
        try:
            imported_data = pd.read_csv(file_path)
            self.leads_df = pd.concat([self.leads_df, imported_data], ignore_index=True)
            self.save_data()
            print(f"Imported {len(imported_data)} leads successfully")
        except Exception as e:
            print(f"Error importing data: {e}")

    def export_to_csv(self, file_path):
        """Export leads to CSV file"""
        try:
            self.leads_df.to_csv(file_path, index=False)
            print(f"Exported {len(self.leads_df)} leads to {file_path}")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def save_data(self):
        """Save leads data to CSV file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.leads_df.to_csv(self.data_file, index=False)


# Demo function
def demo_lead_management():
    lm = LeadManager()

    # Create sample leads
    lm.create_lead("John Doe", "john@example.com", "123-456-7890", "Tech Corp")
    lm.create_lead("Jane Smith", "jane@example.com", "098-765-4321", "Sales Inc")

    # Read all leads
    lm.read_leads()

    # Update a lead
    lm.update_lead(1, notes="Interested in product demo")

    # Move lead through pipeline
    lm.move_lead_stage(1, "Contacted")
    lm.move_lead_stage(1, "Qualified")

    # Read leads again
    lm.read_leads()


if __name__ == "__main__":
    demo_lead_management()
