type = ['primary', 'info', 'success', 'warning', 'danger'];

// Line Chart - Features a bit of filling
gradientChartOptionsConfiguration = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },
  animation: {
    duration: 2500,
  },
  tooltips: {
    bodySpacing: 4,
    mode: "nearest",
    intersect: 0,
    position: "nearest",
    xPadding: 10,
    yPadding: 10,
    caretPadding: 10
  },
  responsive: true,
  scales: {
    yAxes: [{
      display: 0,
      gridLines: 0,
      ticks: {
        display: false
      },
      gridLines: {
        zeroLineColor: "transparent",
        drawTicks: false,
        display: false,
        drawBorder: false
      }
    }],
    xAxes: [{
      display: 0,
      gridLines: 0,
      ticks: {
        display: false
      },
      gridLines: {
        zeroLineColor: "transparent",
        drawTicks: false,
        display: false,
        drawBorder: false
      }
    }]
  },
  layout: {
    padding: {
      left: 0,
      right: 0,
      top: 15,
      bottom: 15
    }
  }
};

// Line Chart - Blue Tooltip
gradientChartOptionsConfigurationWithTooltipBlue = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },

  animation: {
    duration: 2500,
  },

  tooltips: {
    backgroundColor: '#f5f5f5',
    titleFontColor: '#333',
    bodyFontColor: '#666',
    bodySpacing: 4,
    xPadding: 12,
    mode: "nearest",
    intersect: 0,
    position: "nearest"
  },
  responsive: true,
  scales: {
    yAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.0)',
        zeroLineColor: "transparent",
      },
      ticks: {
        suggestedMin: 60,
        suggestedMax: 125,
        padding: 20,
        fontColor: "#2380f7"
      }
    }],

    xAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.1)',
        zeroLineColor: "transparent",
      },
      ticks: {
        padding: 20,
        fontColor: "#2380f7"
      }
    }]
  }
};

// Line Chart - Purple Tooltip
gradientChartOptionsConfigurationWithTooltipPurple = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },

  animation: {
    duration: 2500,
  },

  tooltips: {
    backgroundColor: '#f5f5f5',
    titleFontColor: '#333',
    bodyFontColor: '#666',
    bodySpacing: 4,
    xPadding: 12,
    mode: "nearest",
    intersect: 0,
    position: "nearest"
  },
  responsive: true,
  scales: {
    yAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.0)',
        zeroLineColor: "transparent",
      },
      ticks: {
        suggestedMin: 60,
        suggestedMax: 125,
        padding: 20,
        fontColor: "#9a9a9a"
      }
    }],

    xAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(225,78,202,0.1)',
        zeroLineColor: "transparent",
      },
      ticks: {
        padding: 20,
        fontColor: "#9a9a9a"
      }
    }]
  }
};

// Line Chart - Orange Tooltip
gradientChartOptionsConfigurationWithTooltipOrange = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },

  animation: {
    duration: 2500,
  },  

  tooltips: {
    backgroundColor: '#f5f5f5',
    titleFontColor: '#333',
    bodyFontColor: '#666',
    bodySpacing: 4,
    xPadding: 12,
    mode: "nearest",
    intersect: 0,
    position: "nearest"
  },
  responsive: true,
  scales: {
    yAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.0)',
        zeroLineColor: "transparent",
      },
      ticks: {
        suggestedMin: 50,
        suggestedMax: 110,
        padding: 20,
        fontColor: "#ff8a76"
      }
    }],

    xAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(220,53,69,0.1)',
        zeroLineColor: "transparent",
      },
      ticks: {
        padding: 20,
        fontColor: "#ff8a76"
      }
    }]
  }
};

// Line Chart - Green Tooltip
gradientChartOptionsConfigurationWithTooltipGreen = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },

  animation: {
    duration: 2500,
  },

  tooltips: {
    backgroundColor: '#f5f5f5',
    titleFontColor: '#333',
    bodyFontColor: '#666',
    bodySpacing: 4,
    xPadding: 12,
    mode: "nearest",
    intersect: 0,
    position: "nearest"
  },
  responsive: true,
  scales: {
    yAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.0)',
        zeroLineColor: "transparent",
      },
      ticks: {
        suggestedMin: 50,
        suggestedMax: 125,
        padding: 20,
        fontColor: "#9e9e9e"
      }
    }],

    xAxes: [{
      barPercentage: 1.6,
      gridLines: {
        drawBorder: false,
        color: 'rgba(0,242,195,0.1)',
        zeroLineColor: "transparent",
      },
      ticks: {
        padding: 20,
        fontColor: "#9e9e9e"
      }
    }]
  }
};

// Bar Chart
gradientBarChartConfiguration = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },

  animation: {
    duration: 2500,
  },

  tooltips: {
    backgroundColor: '#f5f5f5',
    titleFontColor: '#333',
    bodyFontColor: '#666',
    bodySpacing: 4,
    xPadding: 12,
    mode: "nearest",
    intersect: 0,
    position: "nearest"
  },
  responsive: true,
  scales: {
    yAxes: [{

      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.1)',
        zeroLineColor: "transparent",
      },
      ticks: {
        suggestedMin: 60,
        suggestedMax: 120,
        padding: 20,
        fontColor: "#9e9e9e"
      }
    }],

    xAxes: [{

      gridLines: {
        drawBorder: false,
        color: 'rgba(29,140,248,0.1)',
        zeroLineColor: "transparent",
      },
      ticks: {
        padding: 20,
        fontColor: "#9e9e9e"
      }
    }]
  }
};

charts = {
  gradientChart: function(selector, input_labels, input_data) {
    // Chart 1 : gradientChart
    chartColor = "#FFFFFF";
    ctx = document.getElementById(selector).getContext("2d");

    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#80b6f4');
    gradientStroke.addColorStop(1, chartColor);

    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

    var myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {
        labels: input_labels,
        datasets: [{
          label: "Popularity",
          borderColor: "#f96332",
          pointBorderColor: "#FFF",
          pointBackgroundColor: "#f96332",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
          data: input_data
        }]
      },
      options: gradientChartOptionsConfiguration
    });

    return myChart;
  },

  gradientChartWithTooltipPurple: function(selector, input_labels, input_data) {
    // Chart 2 : gradientChartWithTooltipPurple
    var ctx = document.getElementById(selector).getContext("2d");

    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
    gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

    var data = {
      labels: input_labels,
      datasets: [{
        label: "Popularity",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#d048b6',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#d048b6',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#d048b6',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: input_data,
      }]
    };

    var myChart = new Chart(ctx, {
      type: 'line',
      data: data,
      options: gradientChartOptionsConfigurationWithTooltipPurple
    });

    return myChart;    
  },

  gradientChartWithTooltipGreen: function(selector, input_labels, input_data) {
    // Chart 3 : gradientChartWithTooltipGreen
    var ctxGreen = document.getElementById(selector).getContext("2d");

    var gradientStroke = ctxGreen.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
    gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
    gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

    var data = {
      labels: input_labels,
      datasets: [{
        label: "Popularity",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: input_data,
      }]
    };

    var myChart = new Chart(ctxGreen, {
      type: 'line',
      data: data,
      options: gradientChartOptionsConfigurationWithTooltipGreen
    });

    return myChart;
  },

  gradientChartWithTooltipPurpleAlternative: function(selector, input_labels, input_data) {
    // Chart 4 : gradientChartWithTooltipPurpleAlternative    
    var ctx = document.getElementById(selector).getContext('2d');

    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
    gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
    gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

    var config = {
      type: 'line',
      data: {
        labels: input_labels,
        datasets: [{
          label: "Popularity",
          fill: true,
          backgroundColor: gradientStroke,
          borderColor: '#d346b1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          pointBackgroundColor: '#d346b1',
          pointBorderColor: 'rgba(255,255,255,0)',
          pointHoverBackgroundColor: '#d346b1',
          pointBorderWidth: 20,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 15,
          pointRadius: 4,
          data: input_data,
        }]
      },
      options: gradientChartOptionsConfigurationWithTooltipPurple
    };

    var myChart = new Chart(ctx, config);

    return myChart;
  },

  gradientBarChart: function(selector, input_labels, input_data) {
    // Chart 5 : gradientBarChart     
    var ctx = document.getElementById(selector).getContext("2d");

    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

    var myChart = new Chart(ctx, {
      type: 'bar',
      responsive: true,
      legend: {
        display: false
      },
      data: {
        labels: input_labels,
        datasets: [{
          label: "Popularity",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: input_data,
        }]
      },
      options: gradientBarChartConfiguration
    });    

    return myChart;
  },
};