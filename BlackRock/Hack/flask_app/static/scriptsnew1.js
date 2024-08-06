document.addEventListener("DOMContentLoaded", () => {
  fetchPortfolio();
  document.getElementById("logout-button").addEventListener("click", () => {
    window.location.href = "/logout";
  });

  document.getElementById("search-button").addEventListener("click", () => {
    const stockSymbol = document.getElementById("stock-symbol").value;
    if (stockSymbol) {
      document.getElementById("trade-options").style.display = "flex";
    }
  });

  document.getElementById("buy-button").addEventListener("click", () => {
    document.getElementById("trade-form").style.display = "flex";
    document.getElementById("confirm-buy-button").style.display =
      "inline-block";
    document.getElementById("confirm-sell-button").style.display = "none";
  });

  document.getElementById("sell-button").addEventListener("click", () => {
    document.getElementById("trade-form").style.display = "flex";
    document.getElementById("confirm-sell-button").style.display =
      "inline-block";
    document.getElementById("confirm-buy-button").style.display = "none";
  });

  document
    .getElementById("confirm-buy-button")
    .addEventListener("click", () => {
      const stockSymbol = document.getElementById("stock-symbol").value;
      const quantity = document.getElementById("quantity").value;
      if (stockSymbol && quantity) {
        buyStock(stockSymbol, quantity);
      }
    });

  document
    .getElementById("confirm-sell-button")
    .addEventListener("click", () => {
      const stockSymbol = document.getElementById("stock-symbol").value;
      const quantity = document.getElementById("quantity").value;
      if (stockSymbol && quantity) {
        sellStock(stockSymbol, quantity);
      }
    });
}),
  document.addEventListener("DOMContentLoaded", () => {
    document
      .getElementById("new-user-form")
      .addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent the default form submission

        const newUsername = document.getElementById("new-username").value;
        if (newUsername) {
          createUser(newUsername);
        }
      });
  });

function fetchPortfolio() {
  fetch("/portfolio")
    .then((response) => response.json())
    .then((data) => {
      const portfolioBody = document.getElementById("portfolio-body");
      portfolioBody.innerHTML = "";
      data.portfolio.forEach((item) => {
        const row = document.createElement("tr");
        row.innerHTML = `
                    <td>${item.stock_symbol}</td>
                    <td>${item.quantity}</td>
                    <td>${item.buy_price.toFixed(2)}</td>
                    <td>${item.current_price.toFixed(2)}</td>
                    <td>${item.value.toFixed(2)}</td>
                `;
        portfolioBody.appendChild(row);
      });

      document.getElementById("total-invested").textContent =
        data.total_invested.toFixed(2);
      document.getElementById("total-current-value").textContent =
        data.total_current_value.toFixed(2);
      document.getElementById("total-returns").textContent = (
        data.total_current_value - data.total_invested
      ).toFixed(2);
      document.getElementById("percentage-gain").textContent =
        (
          ((data.total_current_value - data.total_invested) /
            data.total_invested) *
          100
        ).toFixed(2) + "%";
      document.getElementById("one-day-returns").textContent =
        data.one_day_returns.toFixed(2);
    });
}

function buyStock(stockSymbol, quantity) {
  fetch("/buy", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ stock_symbol: stockSymbol, quantity: quantity }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      fetchPortfolio();
      resetTradeForm();
    });
}

function sellStock(stockSymbol, quantity) {
  fetch("/sell", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ stock_symbol: stockSymbol, quantity: quantity }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      fetchPortfolio();
      resetTradeForm();
    });
}

function createUser(username) {
  fetch("/create_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username: username }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function resetTradeForm() {
  document.getElementById("trade-options").style.display = "none";
  document.getElementById("trade-form").style.display = "none";
  document.getElementById("quantity").value = "";
}
