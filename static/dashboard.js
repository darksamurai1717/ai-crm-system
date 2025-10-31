// Dashboard JavaScript - Updated with Vibrant Colors
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    setInterval(loadDashboardData, 30000);
});

function loadDashboardData() {
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            updateKPIs(data.kpis);
            updateCharts(data);
            updateActivities(data.recent_activities);
        })
        .catch(error => console.error('Error loading dashboard data:', error));
}

function updateKPIs(kpis) {
    document.getElementById('total-revenue').textContent =
        new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(kpis.total_revenue || 0);

    document.getElementById('conversion-rate').textContent = (kpis.conversion_rate || 0).toFixed(1) + '%';
    document.getElementById('churn-rate').textContent = (kpis.churn_rate || 0).toFixed(1) + '%';
    document.getElementById('total-leads').textContent = kpis.total_leads || 0;
    document.getElementById('active-deals').textContent = kpis.active_deals || 0;
}

function updateCharts(data) {
    // Revenue Trend Chart - Cyan/Teal Gradient
    const revenueCtx = document.getElementById('revenueChart');
    if (revenueCtx) {
        if (window.revenueChartInstance) {
            window.revenueChartInstance.destroy();
        }

        window.revenueChartInstance = new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: (data.revenue_trend || []).map(d => d.month),
                datasets: [{
                    label: 'Revenue',
                    data: (data.revenue_trend || []).map(d => d.revenue),
                    borderColor: '#00D9FF',
                    backgroundColor: 'rgba(0, 217, 255, 0.15)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#00D9FF',
                    pointBorderColor: 'white',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: 'white', font: { size: 12, weight: 'bold' } }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgba(255,255,255,0.7)',
                            callback: function(value) {
                                return '$' + (value / 1000) + 'K';
                            }
                        },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    x: {
                        ticks: { color: 'rgba(255,255,255,0.7)' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    }
                }
            }
        });
    }

    // Pipeline Chart - Vibrant Multi-color
    const pipelineCtx = document.getElementById('pipelineChart');
    if (pipelineCtx) {
        if (window.pipelineChartInstance) {
            window.pipelineChartInstance.destroy();
        }

        window.pipelineChartInstance = new Chart(pipelineCtx, {
            type: 'doughnut',
            data: {
                labels: (data.pipeline_data || []).map(d => d.stage),
                datasets: [{
                    data: (data.pipeline_data || []).map(d => d.count),
                    backgroundColor: [
                        '#FF6B6B',    // Red
                        '#4ECDC4',    // Teal
                        '#45B7D1',    // Blue
                        '#FFA07A',    // Salmon
                        '#98D8C8'     // Mint
                    ],
                    borderColor: 'rgba(30, 27, 46, 0.9)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: 'white', font: { size: 12, weight: 'bold' } }
                    }
                }
            }
        });
    }

    // Top Reps Bar Chart - Vibrant Green/Blue
    const topRepsCtx = document.getElementById('topRepsChart');
    if (topRepsCtx) {
        if (window.topRepsChartInstance) {
            window.topRepsChartInstance.destroy();
        }

        window.topRepsChartInstance = new Chart(topRepsCtx, {
            type: 'bar',
            data: {
                labels: ['Rep 1', 'Rep 2', 'Rep 3', 'Rep 4'],
                datasets: [{
                    label: 'Deals Won',
                    data: [12, 9, 8, 6],
                    backgroundColor: [
                        '#00D9FF',    // Cyan
                        '#45B7D1',    // Blue
                        '#00C9A7',    // Teal
                        '#FF6B9D'     // Pink
                    ],
                    borderColor: 'rgba(255,255,255,0.3)',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: 'white', font: { size: 12, weight: 'bold' } }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: 'rgba(255,255,255,0.7)' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    x: {
                        ticks: { color: 'rgba(255,255,255,0.7)' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    }
                }
            }
        });
    }
}

function updateActivities(activities) {
    const container = document.getElementById('activities-container');
    if (!container) return;

    if (!activities || activities.length === 0) {
        container.innerHTML = '<p style="color: rgba(255,255,255,0.7); text-align: center; padding: 1rem;">No recent activities</p>';
        return;
    }

    container.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-type">${activity.type}</div>
            <div class="activity-description">${activity.description}</div>
            ${activity.amount ? `<div style="color: #00D9FF; font-weight: 600; margin-top: 0.25rem;">${activity.amount}</div>` : ''}
        </div>
    `).join('');
}
