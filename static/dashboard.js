// Dashboard JavaScript - InnoStart Style
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
            updateMLInsights(data);
        })
        .catch(error => console.error('Error loading dashboard data:', error));
}

function updateKPIs(kpis) {
    document.getElementById('total-revenue').textContent =
        new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(kpis.total_revenue || 0);

    document.getElementById('conversion-rate').textContent = (kpis.conversion_rate || 0).toFixed(1) + '%';
    document.getElementById('churn-rate').textContent = (kpis.churn_rate || 0).toFixed(1) + '%';
    document.getElementById('total-leads').textContent = kpis.total_leads || 0;
}

function updateCharts(data) {
    // Revenue Trend Chart - Clean Modern Style
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
                    borderColor: '#111827',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366F1',
                    pointBorderColor: '#111827',
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
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#6B7280',
                            font: {
                                size: 12,
                                weight: '600'
                            },
                            callback: function(value) {
                                return '$' + (value / 1000) + 'K';
                            }
                        },
                        grid: {
                            color: '#E5E7EB',
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: '#6B7280',
                            font: {
                                size: 12,
                                weight: '600'
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Pipeline Chart - Modern Doughnut
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
                        '#6366F1',
                        '#10B981',
                        '#F59E0B',
                        '#EF4444',
                        '#8B5CF6'
                    ],
                    borderColor: '#FFFFFF',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#111827',
                            font: {
                                size: 12,
                                weight: '700'
                            },
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
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
        container.innerHTML = '<p style="color: #6B7280; text-align: center; padding: 2rem; font-weight: 500;">No recent activities</p>';
        return;
    }

    container.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-type">${activity.type}</div>
            <div class="activity-description">${activity.description}</div>
            ${activity.amount ? `<div style="color: #10B981; font-weight: 700; margin-top: 0.5rem; font-size: 1.1rem;">${activity.amount}</div>` : ''}
        </div>
    `).join('');
}

function updateMLInsights(data) {
    // Additional ML insights can be updated here if needed
    console.log('ML Insights updated');
}