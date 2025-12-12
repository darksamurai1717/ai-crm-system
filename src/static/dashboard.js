# CORRECTED dashboard.js - FIX FOR MISSING CHARTS

Copy this ENTIRE code to: static/js/dashboard.js

```javascript
// Global variables
const API_BASE = '/api';
let dashboardCharts = {};
let refreshInterval = 30000;

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Dashboard initialized');
    
    // Determine current page and load data
    const path = window.location.pathname;
    
    if (path === '/' || path === '/dashboard') {
        initializeDashboard();
    } else if (path === '/team') {
        initializeTeam();
    } else if (path === '/analytics') {
        initializeAnalytics();
    }
});

// ==================== UTILITY FUNCTIONS ====================

function formatCurrency(value) {
    if (value >= 10000000) {
        return '₹' + (value / 10000000).toFixed(2) + 'Cr';
    } else if (value >= 100000) {
        return '₹' + (value / 100000).toFixed(2) + 'L';
    } else if (value >= 1000) {
        return '₹' + (value / 1000).toFixed(2) + 'K';
    }
    return '₹' + value.toFixed(0);
}

// ==================== DASHBOARD PAGE ====================

function initializeDashboard() {
    loadDashboardData();
    setInterval(loadDashboardData, refreshInterval);
}

function loadDashboardData() {
    console.log('📊 Fetching dashboard data...');
    
    fetch(`${API_BASE}/dashboard-data`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('✅ Dashboard data received:', data);
            
            // Update KPI cards
            updateDashboardKPIs(data.kpis);
            
            // Update charts
            if (data.revenue_trend) updateRevenueChart(data.revenue_trend);
            if (data.pipeline_data) updatePipelineChart(data.pipeline_data);
            
            // Update tables/lists
            if (data.recent_activities) updateActivities(data.recent_activities);
        })
        .catch(error => {
            console.error('❌ Error loading dashboard:', error);
        });
}

function updateDashboardKPIs(kpis) {
    try {
        // Total Revenue
        const revElement = document.getElementById('total-revenue');
        if (revElement) revElement.textContent = formatCurrency(kpis.total_revenue);
        
        // Conversion Rate
        const convElement = document.getElementById('conversion-rate');
        if (convElement) convElement.textContent = (kpis.conversion_rate || 0).toFixed(1);
        
        // Churn Rate
        const churnElement = document.getElementById('churn-rate');
        if (churnElement) churnElement.textContent = (kpis.churn_rate || 0).toFixed(1);
        
        // Total Leads
        const leadsElement = document.getElementById('total-leads');
        if (leadsElement) leadsElement.textContent = kpis.total_leads || 0;
        
        // Active Deals
        const dealsElement = document.getElementById('active-deals');
        if (dealsElement) dealsElement.textContent = kpis.active_deals || 0;
        
        console.log('✅ KPIs updated');
    } catch (error) {
        console.error('Error updating KPIs:', error);
    }
}

function updateRevenueChart(data) {
    try {
        const ctx = document.getElementById('revenueChart');
        if (!ctx) {
            console.warn('⚠️ revenueChart canvas not found');
            return;
        }
        
        // Destroy existing chart if it exists
        if (dashboardCharts.revenue) {
            dashboardCharts.revenue.destroy();
        }
        
        console.log('📈 Creating revenue chart with data:', data);
        
        dashboardCharts.revenue = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.month),
                datasets: [{
                    label: 'Revenue (₹)',
                    data: data.map(d => d.revenue),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
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
                        display: true,
                        labels: { color: '#333' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            },
                            color: '#666'
                        },
                        grid: { color: '#eee' }
                    },
                    x: {
                        ticks: { color: '#666' },
                        grid: { color: '#eee' }
                    }
                }
            }
        });
        console.log('✅ Revenue chart created');
    } catch (error) {
        console.error('Error creating revenue chart:', error);
    }
}

function updatePipelineChart(data) {
    try {
        const ctx = document.getElementById('pipelineChart');
        if (!ctx) {
            console.warn('⚠️ pipelineChart canvas not found');
            return;
        }
        
        // Destroy existing chart
        if (dashboardCharts.pipeline) {
            dashboardCharts.pipeline.destroy();
        }
        
        console.log('🎯 Creating pipeline chart with data:', data);
        
        const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#06b6d4', '#10b981'];
        
        dashboardCharts.pipeline = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.stage),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: colors.slice(0, data.length),
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#333' }
                    }
                }
            }
        });
        console.log('✅ Pipeline chart created');
    } catch (error) {
        console.error('Error creating pipeline chart:', error);
    }
}

function updateActivities(activities) {
    try {
        const feed = document.getElementById('activities-feed');
        if (!feed) return;
        
        feed.innerHTML = activities.slice(0, 5).map(activity => `
            <div class="activity-item">
                <div class="activity-type">${activity.type}</div>
                <div class="activity-desc">${activity.description}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        `).join('');
        console.log('✅ Activities updated');
    } catch (error) {
        console.error('Error updating activities:', error);
    }
}

// ==================== TEAM PAGE ====================

function initializeTeam() {
    loadTeamData();
    setInterval(loadTeamData, refreshInterval);
}

function loadTeamData() {
    console.log('👥 Fetching team data...');
    
    fetch(`${API_BASE}/team-data`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('✅ Team data received:', data);
            
            // Update stats
            updateTeamStats(data.team_stats);
            
            // Update members
            updateTeamMembers(data.team_performance);
            
            // Create chart
            if (data.team_performance) updatePerformanceChart(data.team_performance);
        })
        .catch(error => console.error('❌ Error loading team data:', error));
}

function updateTeamStats(stats) {
    try {
        const updates = {
            'total-members': stats.total_members?.toString() || '0',
            'avg-performance': (stats.avg_performance || 0).toFixed(1) + '/10',
            'team-revenue': formatCurrency(stats.total_revenue || 0),
            'target-achievement': (stats.target_achievement || 0).toFixed(1) + '%'
        };
        
        Object.entries(updates).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        });
        console.log('✅ Team stats updated');
    } catch (error) {
        console.error('Error updating team stats:', error);
    }
}

function updateTeamMembers(members) {
    try {
        members.slice(0, 3).forEach((member, idx) => {
            const num = idx + 1;
            const updates = {
                [`rep${num}-name`]: member.name || 'N/A',
                [`rep${num}-revenue`]: formatCurrency(member.revenue || 0),
                [`rep${num}-deals`]: (member.converted || 0).toString(),
                [`rep${num}-score`]: (member.performance || 0).toFixed(1) + '/10'
            };
            
            Object.entries(updates).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) element.textContent = value;
            });
            
            // Update progress bar
            const progressBar = document.getElementById(`rep${num}-progress`);
            if (progressBar) {
                const percentage = ((member.performance || 0) / 10) * 100;
                progressBar.style.width = percentage + '%';
            }
        });
        console.log('✅ Team members updated');
    } catch (error) {
        console.error('Error updating team members:', error);
    }
}

function updatePerformanceChart(members) {
    try {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) {
            console.warn('⚠️ performanceChart canvas not found');
            return;
        }
        
        if (dashboardCharts.performance) {
            dashboardCharts.performance.destroy();
        }
        
        console.log('📊 Creating performance chart');
        
        dashboardCharts.performance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: members.map(m => m.name),
                datasets: [{
                    label: 'Performance Score (/10)',
                    data: members.map(m => m.performance || 0),
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb'],
                    borderRadius: 6,
                    maxBarThickness: 60
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'x',
                plugins: {
                    legend: { labels: { color: '#333' } }
                },
                scales: {
                    y: { 
                        max: 10,
                        ticks: { color: '#666' },
                        grid: { color: '#eee' }
                    },
                    x: {
                        ticks: { color: '#666' },
                        grid: { color: '#eee' }
                    }
                }
            }
        });
        console.log('✅ Performance chart created');
    } catch (error) {
        console.error('Error creating performance chart:', error);
    }
}

// ==================== ANALYTICS PAGE ====================

function initializeAnalytics() {
    loadAnalyticsData();
    setInterval(loadAnalyticsData, refreshInterval);
}

function loadAnalyticsData() {
    console.log('📈 Fetching analytics data...');
    
    fetch(`${API_BASE}/analytics-data`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('✅ Analytics data received:', data);
            
            // Update KPIs
            updateAnalyticsKPIs(data.kpis);
            
            // Create charts
            if (data.revenue_trend) updateAnalyticsRevenueChart(data.revenue_trend);
            if (data.pipeline) updatePipelineDistributionChart(data.pipeline);
            if (data.churn_risk) updateChurnRiskChart(data.churn_risk);
        })
        .catch(error => console.error('❌ Error loading analytics data:', error));
}

function updateAnalyticsKPIs(kpis) {
    try {
        const updates = {
            'analytics-revenue': formatCurrency(kpis.total_revenue || 0),
            'analytics-conversion': (kpis.conversion_rate || 0).toFixed(1) + '%',
            'analytics-churn': (kpis.churn_rate || 0).toFixed(1) + '%',
            'analytics-growth': (kpis.growth_rate || 0).toFixed(1) + '%'
        };
        
        Object.entries(updates).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        });
        console.log('✅ Analytics KPIs updated');
    } catch (error) {
        console.error('Error updating analytics KPIs:', error);
    }
}

function updateAnalyticsRevenueChart(data) {
    try {
        const ctx = document.getElementById('analyticsRevenueChart');
        if (!ctx) {
            console.warn('⚠️ analyticsRevenueChart canvas not found');
            return;
        }
        
        if (dashboardCharts.analyticsRevenue) {
            dashboardCharts.analyticsRevenue.destroy();
        }
        
        dashboardCharts.analyticsRevenue = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.month),
                datasets: [{
                    label: 'Revenue',
                    data: data.map(d => d.revenue),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#667eea',
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#333' } }
                },
                scales: {
                    y: { 
                        ticks: { color: '#666' },
                        grid: { color: '#eee' }
                    },
                    x: {
                        ticks: { color: '#666' },
                        grid: { color: '#eee' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating analytics revenue chart:', error);
    }
}

function updatePipelineDistributionChart(data) {
    try {
        const ctx = document.getElementById('pipelineDistributionChart');
        if (!ctx) {
            console.warn('⚠️ pipelineDistributionChart canvas not found');
            return;
        }
        
        if (dashboardCharts.pipelineDistribution) {
            dashboardCharts.pipelineDistribution.destroy();
        }
        
        dashboardCharts.pipelineDistribution = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.map(d => d.stage),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: { color: '#333' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating pipeline distribution chart:', error);
    }
}

function updateChurnRiskChart(data) {
    try {
        const ctx = document.getElementById('churnRiskChart');
        if (!ctx) {
            console.warn('⚠️ churnRiskChart canvas not found');
            return;
        }
        
        if (dashboardCharts.churnRisk) {
            dashboardCharts.churnRisk.destroy();
        }
        
        dashboardCharts.churnRisk = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: data,
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#333' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating churn risk chart:', error);
    }
}
```

---

## 🚀 IMPLEMENTATION

1. Copy the entire code above
2. Go to: `static/js/dashboard.js`
3. Delete everything
4. Paste the code
5. Save (Ctrl+S)
6. Refresh browser (Ctrl+F5)

---

## ✅ Expected Result

After updating:
- ✅ All charts will display with data
- ✅ Dashboard tab - revenue & pipeline charts show
- ✅ Team tab - performance bar chart shows
- ✅ Analytics tab - revenue, pipeline, churn charts show
- ✅ Console shows "✅" messages confirming data loaded

---

## 🔍 Debugging

Check browser console (F12 → Console):
- Look for "✅" messages - means it worked
- Look for "❌" errors - helps identify issues
- Look for "⚠️" warnings - means canvas not found (HTML issue)