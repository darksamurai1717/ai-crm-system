
// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    initializeCharts();
});

function loadDashboardData() {
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            updateKPIs(data.kpis);
            updateRevenueChart(data.revenue_trend);
            updatePipelineChart(data.pipeline_data);
            updateActivityList(data.recent_activities);
        })
        .catch(error => console.error('Error loading dashboard data:', error));
}

function updateKPIs(kpis) {
    document.getElementById('total-revenue').textContent = 
        new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(kpis.total_revenue);
    document.getElementById('conversion-rate').textContent = kpis.conversion_rate + '%';
    document.getElementById('total-leads').textContent = kpis.total_leads.toLocaleString();
    document.getElementById('active-deals').textContent = kpis.active_deals;
}

function updateActivityList(activities) {
    const activityList = document.getElementById('activity-list');
    activityList.innerHTML = '';

    activities.forEach(activity => {
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `
            <div class="activity-info">
                <div class="activity-type">${activity.type}</div>
                <div class="activity-description">${activity.description}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
            <div class="activity-amount">${activity.amount}</div>
        `;
        activityList.appendChild(activityItem);
    });
}

function initializeCharts() {
    // Revenue Chart will be initialized when data is loaded
}

function updateRevenueChart(revenueData) {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: revenueData.map(d => d.month),
            datasets: [{
                label: 'Revenue',
                data: revenueData.map(d => d.revenue),
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
            plugins: {
                legend: {
                    display: false
                }
            },
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
}

function updatePipelineChart(pipelineData) {
    const ctx = document.getElementById('pipelineChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: pipelineData.map(d => d.stage),
            datasets: [{
                data: pipelineData.map(d => d.count),
                backgroundColor: [
                    '#8b5cf6',
                    '#f59e0b',
                    '#10b981',
                    '#ef4444',
                    '#64748b'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}
        