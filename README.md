

# AI-Powered CRM System

A professional Customer Relationship Management (CRM) platform integrated with advanced Machine Learning capabilities. This system goes beyond traditional data storage by actively predicting customer behavior, scoring leads, and forecasting revenue to drive business growth.

## 📋 Executive Summary

This project allows businesses to leverage data science without needing a dedicated data team. It features a glassmorphism-designed real-time dashboard that visualizes critical metrics and AI-driven insights, helping teams prioritize high-value leads and prevent customer churn.

## 🎯 Key Features

### 🧠 AI & Machine Learning

* **AI Lead Scoring:** Uses a **Random Forest Classifier** (100 trees) to predict conversion probability with 85-90% accuracy.
* **Churn Prediction:** Identifies at-risk customers early using Random Forest and StandardScaler, allowing for proactive retention strategies.
* **Customer Segmentation:** Groups customers into behavioral clusters using **K-Means clustering** (k=3) for targeted marketing.
* **Revenue Forecasting:** Predicts future monthly revenue trends using **Linear Regression** (3-month horizon).

### ⚡ Core Functionality

* **Real-time Analytics Dashboard:** Interactive charts and KPIs updated in real-time.
* **Task Automation:** AI-generated "next-best actions" to guide sales representatives.
* **Team Performance Tracking:** Monitor individual and team-wide sales metrics.
* **Multi-user Authentication:** Secure login system powered by Flask-Login and Werkzeug hashing.
* **Responsive UI:** Modern interface built with HTML5, CSS3, and Glassmorphism design principles.

## 🏗️ Technical Stack

| Component | Technology |
| --- | --- |
| **Backend** | Python 3.13, Flask 2.3 |
| **Machine Learning** | Scikit-learn, Pandas, NumPy |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Chart.js |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Authentication** | Flask-Login |
| **Deployment** | Docker / Heroku (Procfile included) |

## 📂 Project Structure

```bash
ai-crm-system/
├── models/                  # Serialized ML models (.pkl files)
├── src/                     # Source code for helper functions
├── static/                  # CSS, JS, images, and assets
├── templates/               # HTML templates (Jinja2)
├── main_crm_app.py          # Application entry point
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku deployment configuration
├── runtime.txt              # Python runtime version
├── dashboard_summary.csv    # Sample data for dashboard initialization
└── kpi_report.csv           # Sample KPI data

```

## 🚀 Quick Start

### Prerequisites

* Python 3.10 or higher
* Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/darksamurai1717/ai-crm-system.git
cd ai-crm-system

```


2. **Create a Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


4. **Run the Application**
```bash
python main_crm_app.py

```


5. **Access the Dashboard**
Open your browser and navigate to:
`http://127.0.0.1:5000`

## 📊 Model Performance

| Model | Algorithm | Accuracy/Score | Purpose |
| --- | --- | --- | --- |
| **Lead Scoring** | Random Forest | **85-90%** | Prioritize high-value leads |
| **Churn Prediction** | Random Forest | **75-85%** | Alert on retention risks |
| **Revenue Forecast** | Linear Regression | **85%+ (R²)** | Financial planning |
| **Segmentation** | K-Means | **Silhouette > 0.6** | Targeted marketing |



