// Toggle the visibility of the profile menu

function toggleProfileMenu() {
  var menu = document.getElementById("profileMenu");
  if (menu.style.display === "none" || menu.style.display === "") {
    menu.style.display = "block";
  } else {
    menu.style.display = "none";
  }
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
  if (
    !event.target.matches(".profile-button") &&
    !event.target.matches(".profile-name")
  ) {
    var dropdowns = document.getElementsByClassName("profile-menu");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.style.display === "block") {
        openDropdown.style.display = "none";
      }
    }
  }
};

const checkboxes = document.querySelectorAll(".module-checkbox");
const progressBar = document.querySelector(".progress");
const progressPercent = document.getElementById("progressPercent");
const totalModules = checkboxes.length;
const roiSlider = document.getElementById("roiSlider");
const sliderValue = document.getElementById("sliderValue");
const selectedYearElem = document.getElementById("selectedYear");
const amountReturnedElem = document.getElementById("amountReturned");
const investmentChart = document.getElementById("investmentChart");

let selectedYears = 1; // Default value
let chart = null;

checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", updateProgressBar);
});

roiSlider.addEventListener("input", function () {
  sliderValue.textContent = roiSlider.value;
  updateAmountReturned();
});

function updateProgressBar() {
  const checkedCount = document.querySelectorAll(
    ".module-checkbox:checked"
  ).length;
  const progress = (checkedCount / totalModules) * 100;
  progressBar.style.width = `${progress}%`;
  progressPercent.textContent = `${Math.round(progress)}%`;
}

function selectYear(years) {
  selectedYears = years;
  selectedYearElem.textContent = selectedYears;
  updateAmountReturned();
  renderChart();
}

function updateAmountReturned() {
  const initialAmount = parseInt(roiSlider.value, 10);
  const growthRate = 0.07; // Example growth rate of 7%
  const amountReturned =
    initialAmount * Math.pow(1 + growthRate, selectedYears);
  amountReturnedElem.textContent = amountReturned.toFixed(2);
}
// Initialize
updateProgressBar();
updateAmountReturned();
document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("roiSlider");
  const sliderValueDisplay = document.getElementById("sliderValue");
  const selectedYearDisplay = document.getElementById("selectedYear");
  const amountReturnedDisplay = document.getElementById("amountReturned");
  let selectedYear = 1;
  let roiChart;

  // Initialize Chart.js
  function initChart() {
    const ctx = document.getElementById("roiChart").getContext("2d");
    roiChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: generateLabels(selectedYear),
        datasets: [
          {
            label: "Return On FD",
            data: calculateReturns(slider.value, selectedYear, 0.08, true), // 8% return compounded monthly
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            fill: true,
            tension: 0.1,
          },
          {
            label: "Return On Nifty 50",
            data: calculateReturns(slider.value, selectedYear, 0.15, true), // 15% return compounded monthly
            borderColor: "rgba(255, 99, 132, 1)",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            fill: true,
            tension: 0.1,
          },
        ],
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: "YEARS",
            },
          },
          y: {
            title: {
              display: true,
              text: "MONEY",
            },
            beginAtZero: false,
          },
        },
      },
    });
  }

  // Generate labels for the x-axis based on the number of years
  function generateLabels(years) {
    const labels = [];
    for (let i = 0; i <= years; i++) {
      labels.push(i + " Year" + (i === 1 ? "" : "s"));
    }
    return labels;
  }

  // Calculate returns based on the initial investment and the number of years
  function calculateReturns(initialValue, years, annualRate, isMonthly) {
    const data = [];
    let currentValue = 0; // Start at zero since we're adding the initialValue every month
    const monthlyContribution = parseFloat(initialValue); // Monthly contribution
    const periods = isMonthly ? years * 12 : years; // Total compounding periods
    const rate = isMonthly ? annualRate / 12 : annualRate; // Monthly rate if compounded monthly

    for (let i = 0; i <= periods; i++) {
      currentValue = (currentValue + monthlyContribution) * (1 + rate);
      if (i % 12 === 0) {
        // Push data at the end of each year
        data.push(currentValue);
      }
    }

    return data;
  }

  // Update the slider value display
  function updateSliderValue(value) {
    sliderValueDisplay.textContent = value;
    updateChart();
  }

  // Update the selected year and chart data
  function selectYear(year) {
    selectedYear = year;
    selectedYearDisplay.textContent = year;
    updateChart();
  }

  // Update the amount returned based on compound interest with monthly contributions
  function updateAmountReturned() {
    const initialAmount = parseInt(slider.value, 10);
    const growthRate = 0.08; // 8% growth rate
    const monthlyRate = growthRate / 12;
    const months = selectedYear * 12;
    let amountReturned = 0;
    for (let i = 1; i <= months; i++) {
      amountReturned = (amountReturned + initialAmount) * (1 + monthlyRate);
    }
    amountReturnedDisplay.textContent = amountReturned.toFixed(2);
  }

  // Update chart with new data
  function updateChart() {
    const newData1 = calculateReturns(slider.value, selectedYear, 0.08, true); // 8% return compounded monthly
    const newData2 = calculateReturns(slider.value, selectedYear, 0.15, true); // 15% return compounded monthly
    roiChart.data.labels = generateLabels(selectedYear);
    roiChart.data.datasets[0].data = newData1;
    roiChart.data.datasets[1].data = newData2;
    roiChart.update();

    // Update the amount returned display
    updateAmountReturned();
  }

  // Initialize the chart when the page loads
  initChart();

  // Event listeners
  slider.addEventListener("input", function () {
    updateSliderValue(this.value);
  });

  const yearButtons = document.querySelectorAll(".year-button");
  yearButtons.forEach((button) => {
    button.addEventListener("click", function () {
      selectYear(parseInt(this.textContent));
    });
  });
});
