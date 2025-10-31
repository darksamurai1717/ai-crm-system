// Analytics Dashboard JavaScript - Fixed Version with Vibrant Colors
document.addEventListener('DOMContentLoaded', function() {
    loadAnalyticsData();
    setInterval(loadAnalyticsData, 30000);
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
    document.getElementById('analytics-revenue').textContent =
        new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            maximumFractionDigits: 0
        }).format(kpis.total_revenue || 0);

    document.getElementById('analytics-conversion').textContent = (kpis.conversion_rate || 0).toFixed(1) + '%';
    document.getElementById('analytics-churn').textContent = (kpis.churn_rate || 0).toFixed(1) + '%';
    document.getElementById('analytics-growth').textContent = (kpis.growth_rate || 0).toFixed(1) + '%';
}

function updateAnalyticsCharts(data) {
    // Revenue Trend - Cyan/Teal
    const revenueCtx = document.getElementById('analyticsRevenueChart');
    if (revenueCtx) {
        if (window.analyticsRevenueChartInstance) {
            window.analyticsRevenueChartInstance.destroy();
        }

        window.analyticsRevenueChartInstance = new Chart(revenueCtx, {
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
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { labels: { color: 'white', font: { size: 12, weight: 'bold' } } }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgba(255,255,255,0.7)',
                            callback: function(value) { return '$' + (value / 1000) + 'K'; }
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

    // Pipeline Distribution - Multi-color
    const pipelineCtx = document.getElementById('analyticsPipelineChart');
    if (pipelineCtx) {
        if (window.analyticsPipelineChartInstance) {
            window.analyticsPipelineChartInstance.destroy();
        }

        window.analyticsPipelineChartInstance = new Chart(pipelineCtx, {
            type: 'doughnut',
            data: {
                labels: (data.pipeline || []).map(d => d.stage),
                datasets: [{
                    data: (data.pipeline || []).map(d => d.count),
                    backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
                    borderColor: 'rgba(30, 27, 46, 0.9)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { labels: { color: 'white', font: { size: 12, weight: 'bold' } } } }
            }
        });
    }

    // Segment Distribution - Pie Chart
    const segmentCtx = document.getElementById('segmentChart');
    if (segmentCtx) {
        if (window.segmentChartInstance) {
            window.segmentChartInstance.destroy();
        }

        const segmentData = data.segment_dist || {};
        window.segmentChartInstance = new Chart(segmentCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(segmentData),
                datasets: [{
                    data: Object.values(segmentData),
                    backgroundColor: ['#00D9FF', '#45B7D1', '#4ECDC4', '#FF6B9D'],
                    borderColor: 'rgba(30, 27, 46, 0.9)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { labels: { color: 'white', font: { size: 12, weight: 'bold' } } } }
            }
        });
    }

    // Churn Risk Distribution
    const churnCtx = document.getElementById('churnRiskChart');
    if (churnCtx) {
        if (window.churnRiskChartInstance) {
            window.churnRiskChartInstance.destroy();
        }

        window.churnRiskChartInstance = new Chart(churnCtx, {
            type: 'bar',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    label: 'Customers',
                    data: data.churn_risk || [0, 0, 0],
                    backgroundColor: ['#00C9A7', '#FFA07A', '#FF6B6B'],
                    borderColor: 'rgba(255,255,255,0.3)',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: { legend: { labels: { color: 'white', font: { size: 12, weight: 'bold' } } } },
                scales: {
                    x: {
                        ticks: { color: 'rgba(255,255,255,0.7)' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    y: {
                        ticks: { color: 'rgba(255,255,255,0.7)' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    }
                }
            }
        });
    }
}
