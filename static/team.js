// Team Dashboard JavaScript - Updated with Vibrant Colors
document.addEventListener('DOMContentLoaded', function() {
    loadTeamData();
    setInterval(loadTeamData, 30000);
});

function loadTeamData() {
    fetch('/api/team-data')
        .then(response => response.json())
        .then(data => {
            updateTeamStats(data.team_stats);
            updateTeamList(data.team_performance);
            updatePerformanceChart(data.team_performance);
            updateTasksList(data.recent_tasks);
            updateRecommendations(data.team_performance);
        })
        .catch(error => console.error('Error loading team data:', error));
}

function updateTeamStats(stats) {
    document.getElementById('team-size').textContent = stats.total_members || 0;
    document.getElementById('avg-performance').textContent = (stats.avg_performance || 0).toFixed(1) + '%';
    document.getElementById('team-revenue').textContent =
        new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            maximumFractionDigits: 0
        }).format(stats.total_revenue || 0);
    document.getElementById('target-achievement').textContent = (stats.target_achievement || 0).toFixed(1) + '%';
}

function updateTeamList(teamData) {
    const teamList = document.getElementById('team-list');
    if (!teamList) return;

    if (!teamData || teamData.length === 0) {
        teamList.innerHTML = '<p style="color: rgba(255,255,255,0.7); text-align: center; padding: 1rem;">No team data available</p>';
        return;
    }

    teamList.innerHTML = teamData.map(member => `
        <div class="team-member">
            <div class="member-info">
                <div class="member-avatar">${member.name.split(' ').map(n => n[0]).join('')}</div>
                <div class="member-details">
                    <h4>${member.name}</h4>
                    <div class="member-role">${member.role}</div>
                </div>
            </div>
            <div class="member-stats">
                <div class="performance-score">${(member.performance || 0).toFixed(1)}%</div>
                <div class="revenue-info">$${((member.revenue || 0) / 1000).toFixed(0)}K / $${((member.target || 0) / 1000).toFixed(0)}K</div>
            </div>
        </div>
    `).join('');
}

function updatePerformanceChart(teamData) {
    const canvas = document.getElementById('performanceChart');
    if (!canvas) return;

    if (window.performanceChartInstance) {
        window.performanceChartInstance.destroy();
    }

    const names = teamData && teamData.length > 0 ? teamData.map(m => m.name.split(' ')[0]) : ['No Data'];
    const scores = teamData && teamData.length > 0 ? teamData.map(m => m.performance || 0) : [0];

    const ctx = canvas.getContext('2d');
    window.performanceChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: names,
            datasets: [{
                label: 'Performance Score',
                data: scores,
                backgroundColor: [
                    '#FF6B6B',    // Red
                    '#4ECDC4',    // Teal
                    '#45B7D1',    // Blue
                    '#FFA07A',    // Salmon
                    '#98D8C8'     // Mint
                ],
                borderColor: 'rgba(255,255,255,0.3)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: { color: 'white', font: { size: 12, weight: 'bold' } }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: 'rgba(255,255,255,0.7)',
                        callback: function(value) {
                            return value + '%';
                        }
                    },
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

function updateTasksList(tasks) {
    const tasksList = document.getElementById('tasks-list');
    if (!tasksList) return;

    if (!tasks || tasks.length === 0) {
        tasksList.innerHTML = '<p style="color: rgba(255,255,255,0.7); text-align: center; padding: 1rem;">No tasks assigned</p>';
        return;
    }

    tasksList.innerHTML = tasks.map(task => `
        <div class="task-item">
            <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                <div>
                    <div class="task-assignee">${task.assignee}</div>
                    <div class="task-description">${task.task}</div>
                </div>
                <div class="task-priority ${(task.priority || 'Low').toLowerCase()}">${task.priority}</div>
            </div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;">Due: ${task.due}</div>
        </div>
    `).join('');
}

function updateRecommendations(teamData) {
    const recList = document.getElementById('recommendations-list');
    if (!recList) return;

    if (!teamData || teamData.length === 0) {
        recList.innerHTML = '<p style="color: rgba(255,255,255,0.7); text-align: center; padding: 1rem;">No recommendations</p>';
        return;
    }

    const recommendations = [];

    teamData.forEach(member => {
        if (member.performance < 50) {
            recommendations.push({
                type: 'warning',
                text: `${member.name} needs additional support - Performance at ${(member.performance || 0).toFixed(1)}%`
            });
        } else if (member.performance > 85) {
            recommendations.push({
                type: 'success',
                text: `${member.name} is performing exceptionally - Consider promotion/incentive`
            });
        }
    });

    if (recommendations.length === 0) {
        recommendations.push({
            type: 'info',
            text: 'Team is performing well - No urgent actions needed'
        });
    }

    recList.innerHTML = recommendations.map(rec => `
        <div style="padding: 0.75rem; border-left: 3px solid ${rec.type === 'warning' ? '#FF6B6B' : rec.type === 'success' ? '#00C9A7' : '#00D9FF'}; background: rgba(255,255,255,0.05); margin: 0.5rem 0; border-radius: 4px;">
            <div style="color: ${rec.type === 'warning' ? '#FF6B6B' : rec.type === 'success' ? '#00C9A7' : '#00D9FF'}; font-weight: 600; font-size: 0.85rem;">
                ${rec.type === 'warning' ? '⚠️ Action Needed' : rec.type === 'success' ? '✅ Excellence' : 'ℹ️ Info'}
            </div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.25rem;">${rec.text}</div>
        </div>
    `).join('');
}
