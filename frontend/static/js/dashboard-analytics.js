// Dashboard Analytics JavaScript
let activityChart, gestureChart, confidenceChart, hourlyChart;

// Initialize charts on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    loadDashboardData();
    
    // Event listeners
    document.getElementById('time-range').addEventListener('change', loadDashboardData);
    document.getElementById('refresh-data').addEventListener('change', loadDashboardData);
});

function initializeCharts() {
    // Activity Chart (Line Chart)
    const activityCtx = document.getElementById('activity-chart').getContext('2d');
    activityChart = new Chart(activityCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Communications',
                data: [],
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true
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
                        precision: 0
                    }
                }
            }
        }
    });
    
    // Gesture Distribution Chart (Doughnut Chart)
    const gestureCtx = document.getElementById('gesture-chart').getContext('2d');
    gestureChart = new Chart(gestureCtx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    'rgb(59, 130, 246)',
                    'rgb(16, 185, 129)',
                    'rgb(245, 158, 11)',
                    'rgb(239, 68, 68)',
                    'rgb(139, 92, 246)',
                    'rgb(236, 72, 153)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
    
    // Confidence Chart (Bar Chart)
    const confidenceCtx = document.getElementById('confidence-chart').getContext('2d');
    confidenceChart = new Chart(confidenceCtx, {
        type: 'bar',
        data: {
            labels: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
            datasets: [{
                label: 'Gestures',
                data: [],
                backgroundColor: 'rgb(139, 92, 246)',
                barThickness: 30
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
                        precision: 0
                    },
                    max: 1000
                }
            }
        }
    });
    
    // Hourly Usage Chart (Bar Chart)
    const hourlyCtx = document.getElementById('hourly-chart').getContext('2d');
    hourlyChart = new Chart(hourlyCtx, {
        type: 'bar',
        data: {
            labels: ['12AM', '3AM', '6AM', '9AM', '12PM', '3PM', '6PM', '9PM'],
            datasets: [{
                label: 'Usage',
                data: [],
                backgroundColor: 'rgb(16, 185, 129)'
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
                        precision: 0
                    },
                    max: 120
                }
            }
        }
    });
}

async function loadDashboardData() {
    const timeRange = document.getElementById('time-range').value;
    
    try {
        const response = await fetch(`/api/analytics?days=${timeRange}`);
        const data = await response.json();
        
        if (data.success) {
            updateStats(data.stats);
            updateCharts(data.charts);
            updateActivityTable(data.recent_activity);
        } else {
            // Load demo data if API fails
            loadDemoData();
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        loadDemoData();
    }
}

function updateStats(stats) {
    document.getElementById('stat-total').textContent = stats.total_communications || 0;
    document.getElementById('stat-gestures').textContent = stats.total_gestures || 0;
    document.getElementById('stat-confidence').textContent = (stats.avg_confidence || 0) + '%';
    document.getElementById('stat-sessions').textContent = stats.active_sessions || 0;
    
    document.getElementById('stat-total-change').textContent = (stats.total_change || 0) + '%';
    document.getElementById('stat-gestures-change').textContent = (stats.gestures_change || 0) + '%';
    document.getElementById('stat-confidence-change').textContent = (stats.confidence_change || 0) + '%';
    document.getElementById('stat-sessions-change').textContent = (stats.sessions_change || 0) + '%';
}

function updateCharts(charts) {
    // Update Activity Chart
    activityChart.data.labels = charts.activity.labels;
    activityChart.data.datasets[0].data = charts.activity.data;
    activityChart.update();
    
    // Update Gesture Distribution Chart
    gestureChart.data.labels = charts.gestures.labels;
    gestureChart.data.datasets[0].data = charts.gestures.data;
    gestureChart.update();
    
    // Update Confidence Chart
    confidenceChart.data.datasets[0].data = charts.confidence.data;
    confidenceChart.update();
    
    // Update Hourly Chart
    hourlyChart.data.datasets[0].data = charts.hourly.data;
    hourlyChart.update();
}

function updateActivityTable(activities) {
    const tbody = document.getElementById('activity-table');
    
    if (!activities || activities.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-8 text-gray-400">No recent activity</td></tr>';
        return;
    }
    
    tbody.innerHTML = activities.map(activity => `
        <tr class="border-b hover:bg-gray-50">
            <td class="py-3 px-4">${activity.time}</td>
            <td class="py-3 px-4">${activity.type}</td>
            <td class="py-3 px-4">${activity.gesture}</td>
            <td class="py-3 px-4">
                <span class="px-2 py-1 rounded ${getConfidenceClass(activity.confidence)}">
                    ${activity.confidence}%
                </span>
            </td>
            <td class="py-3 px-4 max-w-xs truncate">${activity.output}</td>
            <td class="py-3 px-4">
                <span class="px-2 py-1 rounded ${getStatusClass(activity.status)}">
                    ${activity.status}
                </span>
            </td>
        </tr>
    `).join('');
}

function getConfidenceClass(confidence) {
    if (confidence >= 80) return 'bg-green-100 text-green-800';
    if (confidence >= 60) return 'bg-blue-100 text-blue-800';
    if (confidence >= 40) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
}

function getStatusClass(status) {
    if (status === 'Success') return 'bg-green-100 text-green-800';
    if (status === 'Processing') return 'bg-blue-100 text-blue-800';
    return 'bg-gray-100 text-gray-800';
}

function loadDemoData() {
    // Demo stats
    updateStats({
        total_communications: 1247,
        total_gestures: 3891,
        avg_confidence: 87,
        active_sessions: 12,
        total_change: 15.3,
        gestures_change: 22.1,
        confidence_change: 5.2,
        sessions_change: 8.7
    });
    
    // Demo charts data
    const daysInRange = parseInt(document.getElementById('time-range').value);
    const activityLabels = [];
    const activityData = [];
    
    for (let i = daysInRange - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        activityLabels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        activityData.push(Math.floor(Math.random() * 50) + 20);
    }
    
    updateCharts({
        activity: {
            labels: activityLabels,
            data: activityData
        },
        gestures: {
            labels: ['Hello', 'Thank You', 'Help', 'Yes', 'No', 'Other'],
            data: [450, 320, 180, 290, 150, 210]
        },
        confidence: {
            data: [45, 120, 280, 520, 890]
        },
        hourly: {
            data: [12, 8, 15, 45, 78, 92, 65, 38]
        }
    });
    
    // Demo activity table
    updateActivityTable([
        {
            time: '2 mins ago',
            type: 'Gesture',
            gesture: 'Hello',
            confidence: 92,
            output: 'Hello, how are you?',
            status: 'Success'
        },
        {
            time: '5 mins ago',
            type: 'Gesture',
            gesture: 'Thank You',
            confidence: 88,
            output: 'Thank you very much',
            status: 'Success'
        },
        {
            time: '12 mins ago',
            type: 'Gesture',
            gesture: 'Help',
            confidence: 75,
            output: 'I need help',
            status: 'Success'
        },
        {
            time: '18 mins ago',
            type: 'Gesture',
            gesture: 'Yes',
            confidence: 95,
            output: 'Yes, I agree',
            status: 'Success'
        },
        {
            time: '25 mins ago',
            type: 'Gesture',
            gesture: 'No',
            confidence: 82,
            output: 'No, thank you',
            status: 'Success'
        }
    ]);
}
