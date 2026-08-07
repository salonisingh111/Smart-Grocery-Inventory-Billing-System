document.addEventListener('DOMContentLoaded', () => {
  const salesCanvas = document.getElementById('salesChart');
  const catCanvas = document.getElementById('categoryChart');

  if (!salesCanvas || !catCanvas) return;

  fetch('/api/dashboard/chart-data')
    .then(res => res.json())
    .then(data => {
      // Sales & Revenue Trend Chart
      new Chart(salesCanvas, {
        type: 'line',
        data: {
          labels: data.sales.labels,
          datasets: [
            {
              label: 'Revenue (₹)',
              data: data.sales.revenue,
              borderColor: '#2563eb',
              backgroundColor: 'rgba(37, 99, 235, 0.1)',
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
          plugins: { legend: { position: 'top' } }
        }
      });

      // Category Distribution Chart
      new Chart(catCanvas, {
        type: 'doughnut',
        data: {
          labels: data.categories.labels,
          datasets: [{
            data: data.categories.values,
            backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { position: 'bottom' } }
        }
      });
    })
    .catch(err => console.error('Error loading dashboard charts:', err));
});
