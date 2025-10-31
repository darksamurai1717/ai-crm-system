from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route('/analytics')
def analytics():
    return render_template('analytics_dashboard.html')

# API endpoint for dashboard data
@app.route('/api/analytics-data')
def analytics_data():
    # Real data: load from models or CSVs. Here is sample data:
    return jsonify({
        "kpis": {
            "total_revenue": 1850000,
            "conversion_rate": 62.3,
            "churn_rate": 9.3,
            "growth_rate": 19.7
        },
        "revenue_trend": [
            {"month": "Jan", "revenue": 235000},
            {"month": "Feb", "revenue": 288000},
            {"month": "Mar", "revenue": 325000},
            {"month": "Apr", "revenue": 298000},
            {"month": "May", "revenue": 367000},
            {"month": "Jun", "revenue": 399000}
        ],
        "pipeline": [
            {"stage": "New", "count": 142},
            {"stage": "Contacted", "count": 128},
            {"stage": "Qualified", "count": 106},
            {"stage": "Converted", "count": 92},
            {"stage": "Lost", "count": 76}
        ],
        "segment_dist": {
            "High Value": 55,
            "Trial": 32,
            "Enterprise": 17,
            "Low Engagement": 29
        },
        "churn_risk": [34, 18, 9]  # [Low, Medium, High]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
