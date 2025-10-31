// Real-time Dashboard Updates
class RealTimeDashboard {
    constructor(updateInterval = 30000) { // 30 seconds
        this.updateInterval = updateInterval;
        this.isRunning = false;
    }

    start() {
        this.isRunning = true;
        this.update();
        this.intervalId = setInterval(() => this.update(), this.updateInterval);
        console.log('🔄 Real-time updates started');
    }

    stop() {
        this.isRunning = false;
        clearInterval(this.intervalId);
        console.log('⏸️ Real-time updates stopped');
    }

    async update() {
        if (!this.isRunning) return;

        try {
            // Show loading indicator
            this.showUpdateIndicator();

            // Fetch fresh data
            const response = await fetch('/api/dashboard-data');
            const data = await response.json();

            // Update KPIs
            this.updateKPIs(data.kpis);

            // Update charts
            this.updateCharts(data);

            // Hide loading indicator
            this.hideUpdateIndicator();

            console.log('✅ Dashboard updated', new Date().toLocaleTimeString());
        } catch (error) {
            console.error('❌ Update failed:', error);
        }
    }

    showUpdateIndicator() {
        const indicator = document.querySelector('.live-indicator');
        if (indicator) {
            indicator.innerHTML = '<span class="loading-spinner"></span> Updating...';
        }
    }

    hideUpdateIndicator() {
        const indicator = document.querySelector('.live-indicator');
        if (indicator) {
            indicator.innerHTML = '<span class="live-dot"></span> Live';
        }
    }

    updateKPIs(kpis) {
        // Animate number changes
        this.animateValue('total-revenue', kpis.total_revenue);
        this.animateValue('conversion-rate', kpis.conversion_rate);
        this.animateValue('churn-rate', kpis.churn_rate);
        this.animateValue('total-leads', kpis.total_leads);
    }

    animateValue(id, endValue) {
        const element = document.getElementById(id);
        if (!element) return;

        const startValue = parseFloat(element.textContent.replace(/[^0-9.-]+/g, ''));
        const duration = 1000; // 1 second
        const startTime = Date.now();

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const currentValue = startValue + (endValue - startValue) * progress;
            element.textContent = this.formatValue(id, currentValue);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        animate();
    }

    formatValue(id, value) {
        if (id === 'total-revenue') {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                maximumFractionDigits: 0
            }).format(value);
        } else if (id.includes('rate')) {
            return value.toFixed(1) + '%';
        } else {
            return Math.round(value).toString();
        }
    }

    updateCharts(data) {
        // You can add chart update logic here
        console.log('Charts data received:', data);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const dashboard = new RealTimeDashboard(30000); // Update every 30 seconds
    dashboard.start();

    // Add start/stop controls
    window.realtimeDashboard = dashboard;
});
