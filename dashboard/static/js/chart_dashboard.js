function charsMensual(data) {
 
  // Extraer los datos que necesitas
  const labels = data.map(item => item.month_name); // Usar el nombre del mes como etiqueta
  const gastos = data.map(item => parseFloat(item.gasto)); // Convertir 'gasto' a número
  const ingresos = data.map(item => parseFloat(item.ingreso)); // Convertir 'ingreso' a número
  const ahorros = data.map(item => parseFloat(item.ahorro)); // Convertir 'ahorro' a número

  const ctx = document.getElementById('myAreaChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Gastos',
          data: gastos,
          backgroundColor: 'rgba(255, 99, 71, 0.6)', // Tomato
          borderColor: 'rgba(255, 99, 71, 1)', // Tomato (border)
          borderWidth: 1
        },
        {
          label: 'Ingresos',
          data: ingresos,
          backgroundColor: 'rgba(30, 144, 255, 0.6)', // Dodger Blue
          borderColor: 'rgba(30, 144, 255, 1)', // Dodger Blue (border)
          borderWidth: 1
        },
        {
          label: 'Ahorros',
          data: ahorros,
          backgroundColor: 'rgba(60, 179, 113, 0.6)', // Medium Sea Green
          borderColor: 'rgba(60, 179, 113, 1)', // Medium Sea Green (border)
          borderWidth: 1
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Monto (en unidades monetarias)'
          }
        },
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
        }
      }
    }
  });
}



function charsAhorroMensual(data) {
 
  // Extraer los datos que necesitas
  const labels = data.map(item => item.month_name); // Usar el nombre del mes como etiqueta
  const ahorros = data.map(item => parseFloat(item.ahorro)); // Convertir 'ahorro' a número

  const ctx = document.getElementById('myBarChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Ahorros',
          data: ahorros,
          backgroundColor: 'rgba(60, 179, 113, 0.6)', // Medium Sea Green
          borderColor: 'rgba(60, 179, 113, 1)', // Medium Sea Green (border)
          borderWidth: 1
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Monto (en unidades monetarias)'
          }
        },
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
        }
      }
    }
  });
}


function charsProporcion(data) {
  const ctx = document.getElementById('myProporcion');
  ctx.width = 545;
  ctx.height = 545;

  // Extracting categories and total amounts from the data
  const labels = data.map(item => item.category);
  const amounts = data.map(item => parseFloat(item.total_amount));

  new Chart(ctx, {
    type: 'pie',
    data: {
      datasets: [
        {
          data: amounts,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(255, 99, 71)',
          ],
          label: 'Financial Data',
        },
      ],
      labels: labels,
    },
    options: {
      plugins: {
        legend: {
          position: 'right',
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              const dataset = tooltipItem.chart.data.datasets[tooltipItem.datasetIndex];
              const total = dataset.data.reduce((prev, curr) => prev + curr);
              const currentValue = dataset.data[tooltipItem.dataIndex];
              const percentage = Math.round((currentValue / total) * 100);
              return `${currentValue} (${percentage}%)`;
            }
          }
        },
        datalabels: {
          formatter: (value, ctx) => {
            const dataset = ctx.chart.data.datasets[ctx.datasetIndex];
            const total = dataset.data.reduce((acc, data) => acc + data, 0);
            const percentage = Math.round((value / total) * 100) + '%';
            return percentage;
          },
          color: '#fff'
        }
      }
    }
  });
}

