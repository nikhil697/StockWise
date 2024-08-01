// Mock data and functions for demonstration purposes
const initialAmount = 500000; // ₹5,00,000
let amountLeft = initialAmount;

const portfolio = [
    { name: "Company A", ticker: "COMPA", boughtPrice: 100, currentPrice: 120, quantity: 10, investedAmount: 1000, currentValue: 1200 },
    { name: "Company B", ticker: "COMPB", boughtPrice: 200, currentPrice: 180, quantity: 10, investedAmount: 2000, currentValue: 1800 }
];

function updatePortfolio() {
    const portfolioContainer = document.getElementById('portfolio-companies');
    portfolioContainer.innerHTML = '';

    portfolio.forEach(stock => {
        const stockElement = document.createElement('div');
        stockElement.className = 'portfolio-item';
        stockElement.innerHTML = `
            <span>${stock.name} (${stock.ticker})</span>
            <span>₹${stock.boughtPrice.toFixed(2)}</span>
            <span>₹${stock.currentPrice.toFixed(2)}</span>
            <span>${stock.quantity}</span>
        `;
        portfolioContainer.appendChild(stockElement);
    });

    const investedAmount = portfolio.reduce((sum, stock) => sum + stock.investedAmount, 0);
    const currentValue = portfolio.reduce((sum, stock) => sum + stock.currentValue, 0);

    document.getElementById('invested-amount').textContent = `₹${investedAmount.toFixed(2)}`;
    document.getElementById('current-value').textContent = `₹${currentValue.toFixed(2)}`;
    document.getElementById('amount-left').textContent = `₹${(amountLeft - investedAmount).toFixed(2)}`;
}

function searchStock() {
    const query = document.getElementById('search-input').value;
    // Mock search result
    const stock = { name: "Company C", ticker: "COMPC", price: 150, marketCap: 500000 };

    if (query.toLowerCase() === stock.ticker.toLowerCase() || query.toLowerCase() === stock.name.toLowerCase()) {
        showStockDetails(stock);
    } else {
        alert('Stock not found');
    }
}

function showStockDetails(stock) {
    const stockDetailsContainer = document.getElementById('stock-details');
    stockDetailsContainer.innerHTML = `
        <h2>${stock.name} (${stock.ticker})</h2>
        <p>Price: ₹${stock.price}</p>
        <p>Market Cap: ₹${stock.marketCap}</p>
        <button class="buy" onclick="buyStock('${stock.ticker}', ${stock.price})">Buy</button>
        <button class="sell" onclick="sellStock('${stock.ticker}', ${stock.price})">Sell</button>
    `;
}

function buyStock(ticker, price) {
    // Implement the buy logic
    alert(`Buying stock: ${ticker} at ₹${price}`);
}

function sellStock(ticker, price) {
    // Implement the sell logic
    alert(`Selling stock: ${ticker} at ₹${price}`);
}

// Initial load
updatePortfolio();
