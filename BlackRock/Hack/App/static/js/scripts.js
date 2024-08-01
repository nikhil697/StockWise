const initialAmount = 500000; // ₹5,00,000
let amountLeft = initialAmount;

const portfolio = [];

async function fetchPortfolio() {
  const response = await fetch("/mockstock/");
  const data = await response.json();

  if (response.ok) {
    portfolio.length = 0;
    data.portfolio.forEach((stock) => {
      portfolio.push({
        name: stock.stock_name,
        ticker: stock.stock_name, // Assuming stock_name as ticker for demo purposes
        boughtPrice: stock.bought_price,
        currentPrice: stock.current_price,
        quantity: stock.quantity,
        investedAmount: stock.bought_price * stock.quantity,
        currentValue: stock.current_price * stock.quantity,
      });
    });
    updatePortfolio();
  } else {
    alert(data.error || "Failed to fetch portfolio data");
  }
}

function updatePortfolio() {
  const portfolioContainer = document.getElementById("portfolio-companies");
  portfolioContainer.innerHTML = "";

  portfolio.forEach((stock) => {
    const stockElement = document.createElement("div");
    stockElement.className = "portfolio-item";
    stockElement.innerHTML = `
            <span>${stock.name}</span>
            <span>₹${stock.boughtPrice.toFixed(2)}</span>
            <span>₹${stock.currentPrice.toFixed(2)}</span>
            <span>${stock.quantity}</span>
            <button onclick="sellStock('${stock.ticker}', ${
      stock.currentPrice
    })">Sell</button>
        `;
    portfolioContainer.appendChild(stockElement);
  });

  const investedAmount = portfolio.reduce(
    (sum, stock) => sum + stock.investedAmount,
    0
  );
  const currentValue = portfolio.reduce(
    (sum, stock) => sum + stock.currentValue,
    0
  );

  document.getElementById(
    "invested-amount"
  ).textContent = `₹${investedAmount.toFixed(2)}`;
  document.getElementById(
    "current-value"
  ).textContent = `₹${currentValue.toFixed(2)}`;
  document.getElementById("amount-left").textContent = `₹${(
    amountLeft - investedAmount
  ).toFixed(2)}`;
}

async function searchStock() {
  const query = document.getElementById("search-input").value;
  const response = await fetch(`/App/stock/?ticker=${query}`);
  const stock = await response.json();
  showStockDetails(stock);
}

function showStockDetails(stock) {
  const stockDetailsContainer = document.getElementById("stock-details");
  stockDetailsContainer.innerHTML = `
        <h2>${stock.name} (${stock.ticker})</h2>
        <p>Price: ₹${stock.price}</p>
        <p>Market Cap: ₹${stock.marketCap}</p>
        <input type="range" id="quantity-slider" min="1" max="100" value="1" oninput="updateQuantity(this.value)">
        <span id="quantity-value">1</span>
        <button class="buy" onclick="buyStock('${stock.ticker}', ${stock.price})">Buy</button>
    `;
}

function updateQuantity(quantity) {
  document.getElementById("quantity-value").textContent = quantity;
}

function buyStock(ticker, price) {
  const quantity = document.getElementById("quantity-slider").value;
  const investedAmount = price * quantity;

  if (investedAmount <= amountLeft) {
    amountLeft -= investedAmount;
    portfolio.push({
      name: ticker,
      ticker: ticker,
      boughtPrice: price,
      currentPrice: price,
      quantity: parseInt(quantity),
      investedAmount: investedAmount,
      currentValue: investedAmount,
    });
    updatePortfolio();
  } else {
    alert("Insufficient funds to buy this stock");
  }
}

function sellStock(ticker, price) {
  const stockIndex = portfolio.findIndex((stock) => stock.ticker === ticker);
  if (stockIndex >= 0) {
    const stock = portfolio[stockIndex];
    const investedAmount = stock.quantity * price;
    amountLeft += investedAmount;
    portfolio.splice(stockIndex, 1);
    updatePortfolio();
  } else {
    alert("Stock not found in the portfolio");
  }
}

// Initial load
document.addEventListener("DOMContentLoaded", fetchPortfolio);
