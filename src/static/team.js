
// Team Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadTeamData();
});

function loadTeamData() {
    fetch('/api/team-data')
        .then(response => response.json())
        .then(data => {
            updateTeamStats(data.team_stats);
            updateTeamList(data.team_performance);
            updateTasksList(data.recent_tasks);
            updatePerformanceChart(data.team_performance);
        })
        .catch(error => console.error('Error loading team data:', error));
}

function updateTeamStats(stats) {
    document.getElementById('team-size').textContent = stats.total_members;
    document.getElementById('avg-performance').textContent = stats.avg_performance + '%';
    document.getElementById('team-revenue').textContent = 
        new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(stats.total_revenue);
    document.getElementById('target-achievement').textContent = stats.target_achievement + '%';
}

function updateTeamList(teamData) {
    const teamList = document.getElementById('team-list');
    teamList.innerHTML = '';

    teamData.forEach(member => {
        const memberElement = document.createElement('div');
        memberElement.className = 'team-member';
        memberElement.innerHTML = `
            <div class="member-info">
                <div class="member-avatar">${member.name.split(' ').map(n => n[0]).join('')}</div>
                <div class="member-details">
                    <h4>${member.name}</h4>
                    <div class="member-role">${member.role}</div>
                </div>
            </div>
            <div class="member-stats">
                <div class="performance-score">${member.performance.toFixed(1)}%</div>
                <div class="revenue-info">$${(member.revenue / 1000).toFixed(0)}K / $${(member.target / 1000).toFixed(0)}K</div>
            </div>
        `;
        teamList.appendChild(memberElement);
    });
}

function updateTasksList(tasks) {
    const tasksList = document.getElementById('tasks-list');
    tasksList.innerHTML = '';

    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task-item';
        taskElement.innerHTML = `
            <div class="task-details">
                <div class="task-assignee">${task.assignee}</div>
                <div class="task-description">${task.task}</div>
                <div class="task-priority ${task.priority.toLowerCase()}">${task.priority}</div>
            </div>
            <div class="task-due">${task.due}</div>
        `;
        tasksList.appendChild(taskElement);
    });
}

function updatePerformanceChart(teamData) {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: teamData.map(member => member.name.split(' ')[0]),
            datasets: [{
                label: 'Performance Score',
                data: teamData.map(member => member.performance),
                backgroundColor: 'rgba(139, 92, 246, 0.8)',
                borderColor: '#8b5cf6',
                borderWidth: 1,
                borderRadius: 8
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
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}
        