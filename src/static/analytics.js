document.addEventListener('DOMContentLoaded', function() {
    loadAnalyticsData();
});

function loadAnalyticsData() {
    fetch('/api/analytics-data')
        .then(response => response.json())
        .then(data => {
            updateAnalyticsKPIs(data.kpis);
            updateAnalyticsCharts(data);
        })
        .catch(error => console.error('Error loading analytics data:', error));
}

function updateAnalyticsKPIs(kpis) {
    document.getElementById('total-revenue').textContent =
        new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(kpis.total_revenue);
    document.getElementById('conversion-rate').textContent = kpis.conversion_rate + '%';
    document.getElementById('churn-rate').textContent = kpis.churn_rate + '%';
    document.getElementById('growth-rate').textContent = kpis.growth_rate + '%';
}

function updateAnalyticsCharts(data) {
    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: data.revenue_trend.map(d => d.month),
            datasets: [{
                label: 'Revenue',
                data: data.revenue_trend.map(d => d.revenue),
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000) + 'K';
                        }
                    }
                }
            }
        }
    });

    // Pipeline Chart
    const pipelineCtx = document.getElementById('pipelineChart').getContext('2d');
    new Chart(pipelineCtx, {
        type: 'doughnut',
        data: {
            labels: data.pipeline.map(d => d.stage),
            datasets: [{
                data: data.pipeline.map(d => d.count),
                backgroundColor: ['#8b5cf6', '#f59e0b', '#10b981', '#ef4444', '#64748b']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Segment Chart
    const segmentCtx = document.getElementById('segmentChart').getContext('2d');
    new Chart(segmentCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(data.segment_dist),
            datasets: [{
                data: Object.values(data.segment_dist),
                backgroundColor: ['#4facfe', '#f093fb', '#43e97b', '#7353ba']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Churn Chart
    const churnCtx = document.getElementById('churnChart').getContext('2d');
    new Chart(churnCtx, {
        type: 'bar',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            datasets: [{
                label: 'Customers',
                data: data.churn_risk,
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}
