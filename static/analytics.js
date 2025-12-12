// Analytics Dashboard JavaScript - InnoStart Style
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
    // Revenue Trend Chart
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
                    borderColor: '#111827',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#8B5CF6',
                    pointBorderColor: '#111827',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#6B7280',
                            font: { size: 12, weight: '600' },
                            callback: function(value) { return '$' + (value / 1000) + 'K'; }
                        },
                        grid: { color: '#E5E7EB', drawBorder: false }
                    },
                    x: {
                        ticks: { color: '#6B7280', font: { size: 12, weight: '600' } },
                        grid: { display: false }
                    }
                }
            }
        });
    }

    // Pipeline Distribution
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
                    backgroundColor: ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6'],
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
                            font: { size: 12, weight: '700' },
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }

    // Segment Distribution
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
                    backgroundColor: ['#6366F1', '#10B981', '#F59E0B', '#EF4444'],
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
                            font: { size: 12, weight: '700' },
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                }
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
                    backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
                    borderColor: '#FFFFFF',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        ticks: { color: '#6B7280', font: { size: 12, weight: '600' } },
                        grid: { color: '#E5E7EB', drawBorder: false }
                    },
                    y: {
                        ticks: { color: '#6B7280', font: { size: 12, weight: '700' } },
                        grid: { display: false }
                    }
                }
            }
        });
    }
}