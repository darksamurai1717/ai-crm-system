// Team Dashboard JavaScript - InnoStart Style
document.addEventListener('DOMContentLoaded', function() {
    loadTeamData();
    setInterval(loadTeamData, 30000);
});

function loadTeamData() {
    fetch('/api/team-data')
        .then(response => response.json())
        .then(data => {
            updateTeamKPIs(data.team_stats);
            updateTeamTable(data.team_performance);
            updatePerformanceChart(data.team_performance);
            updateTasksList(data.recent_tasks);
        })
        .catch(error => console.error('Error loading team data:', error));
}

function updateTeamKPIs(stats) {
    document.getElementById('team-members').textContent = stats.total_members || 0;
    document.getElementById('avg-performance').textContent = (stats.avg_performance || 0).toFixed(1) + '%';
    document.getElementById('team-revenue').textContent =
        '$' + ((stats.total_revenue || 0) / 1000).toFixed(0) + 'K';
    document.getElementById('target-achievement').textContent = (stats.target_achievement || 0).toFixed(1) + '%';
}

function updateTeamTable(team) {
    const tbody = document.getElementById('team-table');
    if (!tbody) return;

    if (!team || team.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem; color: #6B7280;">No team data available</td></tr>';
        return;
    }

    tbody.innerHTML = team.map(rep => {
        const performanceColor = rep.performance > 80 ? '#10B981' :
                                 rep.performance > 60 ? '#F59E0B' : '#EF4444';
        const statusText = rep.performance > 80 ? 'Excellent' :
                          rep.performance > 60 ? 'Good' : 'Needs Support';
        const statusBg = rep.performance > 80 ? '#D4F4DD' :
                        rep.performance > 60 ? '#FFE8D6' : '#FFB8A8';

        return `
            <tr>
                <td>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <img src="https://i.pravatar.cc/40?u=${rep.name}"
                             style="width: 40px; height: 40px; border-radius: 50%; border: 2px solid #111827;"
                             alt="${rep.name}">
                        <strong style="font-weight: 700;">${rep.name}</strong>
                    </div>
                </td>
                <td style="text-transform: uppercase; font-size: 0.875rem; font-weight: 600; color: #6B7280;">${rep.role}</td>
                <td><strong>${rep.leads_assigned}</strong></td>
                <td><strong style="color: #10B981;">${rep.converted}</strong></td>
                <td><strong style="font-weight: 700;">$${rep.revenue.toLocaleString()}</strong></td>
                <td>
                    <div style="background: ${statusBg}; border-radius: 12px; padding: 0.75rem; text-align: center; border: 2px solid ${performanceColor};">
                        <strong style="color: ${performanceColor}; font-size: 1.1rem;">${rep.performance.toFixed(1)}%</strong>
                    </div>
                </td>
                <td>
                    <span class="badge" style="background: ${statusBg}; color: ${performanceColor}; display: inline-block; padding: 0.5rem 1rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                        ${statusText}
                    </span>
                </td>
            </tr>
        `;
    }).join('');
}

function updatePerformanceChart(team) {
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;

    if (window.performanceChartInstance) {
        window.performanceChartInstance.destroy();
    }

    window.performanceChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: team.map(t => t.name),
            datasets: [{
                label: 'Performance Score',
                data: team.map(t => t.performance),
                backgroundColor: team.map(t =>
                    t.performance > 80 ? '#10B981' :
                    t.performance > 60 ? '#F59E0B' : '#EF4444'
                ),
                borderColor: '#FFFFFF',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    max: 100,
                    ticks: {
                        color: '#6B7280',
                        font: { size: 12, weight: '600' }
                    },
                    grid: { color: '#E5E7EB', drawBorder: false }
                },
                y: {
                    ticks: {
                        color: '#111827',
                        font: { size: 12, weight: '700' }
                    },
                    grid: { display: false }
                }
            }
        }
    });
}

function updateTasksList(tasks) {
    const list = document.getElementById('tasks-list');
    if (!list) return;

    if (!tasks || tasks.length === 0) {
        list.innerHTML = '<div style="padding: 2rem; text-align: center; color: #6B7280; font-weight: 500;">No active tasks</div>';
        return;
    }

    list.innerHTML = tasks.map(task => {
        const priorityColor = task.priority === 'High' ? '#EF4444' :
                             task.priority === 'Medium' ? '#F59E0B' : '#10B981';
        const priorityBg = task.priority === 'High' ? '#FFB8A8' :
                          task.priority === 'Medium' ? '#FFE8D6' : '#D4F4DD';

        return `
            <div class="activity-item">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                    <strong style="font-weight: 700; color: #111827;">${task.assignee}</strong>
                    <span style="font-size: 0.75rem; padding: 0.4rem 0.75rem; border-radius: 50px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
                        background: ${priorityBg}; color: ${priorityColor};">
                        ${task.priority}
                    </span>
                </div>
                <div style="font-size: 0.95rem; color: #6B7280; line-height: 1.5; margin-bottom: 0.5rem;">${task.task}</div>
                <div style="font-size: 0.875rem; color: #9CA3AF; font-weight: 600;">Due: ${task.due}</div>
            </div>
        `;
    }).join('');
}