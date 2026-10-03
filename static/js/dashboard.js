/**
 * NXTWALK Digital Control Center — Dashboard Interactions & Metrics
 */

export function initializeDashboard() {
  const chartContainers = document.querySelectorAll('[data-nxt-chart]');
  if (!chartContainers.length) return;

  function renderChartGradients() {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    const primaryColor = isLight ? '#00b4d8' : '#4ae7ff';
    const secondaryColor = isLight ? '#4361ee' : '#5f8dff';

    chartContainers.forEach((chart) => {
      const bars = chart.querySelectorAll('.chart-bar');
      bars.forEach((bar) => {
        bar.style.background = `linear-gradient(to top, ${secondaryColor} 0%, ${primaryColor} 100%)`;
      });
    });
  }

  renderChartGradients();
  window.addEventListener('nxtwalk:themechange', renderChartGradients);
}
