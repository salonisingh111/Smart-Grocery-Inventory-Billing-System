function updateChartDefaultsForTheme(theme) {
  if (typeof Chart === 'undefined') return;
  const isDark = theme === 'dark' || document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#94A3B8' : '#64748b';
  const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

  if (Chart.defaults) {
    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;
    if (Chart.defaults.scale && Chart.defaults.scale.grid) {
      Chart.defaults.scale.grid.color = gridColor;
    }
  }

  if (typeof Chart.instances !== 'undefined') {
    Object.values(Chart.instances).forEach(chart => {
      if (chart.options) {
        if (chart.options.scales) {
          Object.values(chart.options.scales).forEach(scale => {
            if (scale.grid) scale.grid.color = gridColor;
            if (scale.ticks) scale.ticks.color = textColor;
          });
        }
        if (chart.options.plugins && chart.options.plugins.legend && chart.options.plugins.legend.labels) {
          chart.options.plugins.legend.labels.color = textColor;
        }
        chart.update();
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateChartDefaultsForTheme(document.documentElement.getAttribute('data-theme') || 'light');

  const salesCanvas = document.getElementById('salesChart');
  const catCanvas = document.getElementById('categoryChart');

  if (!salesCanvas || !catCanvas) return;

  fetch('/api/dashboard/chart-data')
    .then(res => res.json())
    .then(data => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const textColor = isDark ? '#94A3B8' : '#64748b';
      const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

      // Sales & Revenue Trend Chart
      new Chart(salesCanvas, {
        type: 'line',
        data: {
          labels: data.sales.labels,
          datasets: [
            {
              label: 'Revenue (₹)',
              data: data.sales.revenue,
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.15)',
              fill: true,
              tension: 0.3
            },
            {
              label: 'Bills Count',
              data: data.sales.values,
              borderColor: '#10b981',
              backgroundColor: 'transparent',
              borderDash: [5, 5],
              tension: 0.3
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: { color: textColor }
            }
          },
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor } }
          }
        }
      });

      // Category Distribution Chart
      new Chart(catCanvas, {
        type: 'doughnut',
        data: {
          labels: data.categories.labels,
          datasets: [{
            data: data.categories.values,
            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: textColor }
            }
          }
        }
      });
    })
    .catch(err => console.error('Error loading dashboard charts:', err));
});
