from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from yahoo_fin import stock_info
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mockstock.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    portfolio = db.relationship('Portfolio', backref='owner', lazy=True)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        return 'Invalid username'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# @app.route('/create_user', methods=['POST'])
# def create_user():
#     data = request.json
#     username = data['username']
#     if User.query.filter_by(username=username).first():
#         return jsonify({'error': 'User already exists'}), 400

#     new_user = User(username=username)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'})

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    username = data['username']
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/buy', methods=['POST'])
@login_required
def buy_stock():
    data = request.json
    stock_symbol = data['stock_symbol']
    quantity = int(data['quantity'])
    price = stock_info.get_live_price(stock_symbol)

    # Check if the stock already exists in the portfolio
    existing_stock = Portfolio.query.filter_by(
        user_id=current_user.id, stock_symbol=stock_symbol
    ).first()

    if existing_stock:
        # Update existing stock entry
        total_quantity = existing_stock.quantity + quantity
        avg_price = (
            (existing_stock.buy_price * existing_stock.quantity + price * quantity) / total_quantity
        )
        existing_stock.quantity = total_quantity
        existing_stock.buy_price = avg_price
    else:
        # Create new stock entry
        new_trade = Portfolio(
            user_id=current_user.id,
            stock_symbol=stock_symbol,
            quantity=quantity,
            buy_price=price
        )
        db.session.add(new_trade)

    db.session.commit()
    return jsonify({'message': 'Stock purchased successfully'})

@app.route('/sell', methods=['POST'])
@login_required
def sell_stock():
    data = request.json
    stock_symbol = data['stock_symbol']
    quantity = int(data['quantity'])

    portfolio_item = Portfolio.query.filter_by(user_id=current_user.id, stock_symbol=stock_symbol).first()
    if not portfolio_item or portfolio_item.quantity < quantity:
        return jsonify({'error': 'Not enough stock to sell'}), 400

    portfolio_item.quantity -= quantity
    if portfolio_item.quantity == 0:
        db.session.delete(portfolio_item)
    db.session.commit()

    return jsonify({'message': 'Stock sold successfully'})

def get_previous_day_close(stock_symbol):
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(days=1)
    try:
        historical_data = stock_info.get_data(stock_symbol, start_date=yesterday, end_date=today)
        return historical_data['close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching previous day's close for {stock_symbol}: {e}")
        return None

@app.route('/portfolio', methods=['GET'])
@login_required
def view_portfolio():
    # Aggregate portfolio data
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).all()
    portfolio_data = []
    total_invested = 0
    total_current_value = 0
    total_day_return = 0

    # Dictionary to aggregate stocks
    stock_aggregation = {}

    for item in portfolio:
        if item.stock_symbol not in stock_aggregation:
            stock_aggregation[item.stock_symbol] = {
                'quantity': 0,
                'total_buy_price': 0,
                'current_price': stock_info.get_live_price(item.stock_symbol),
                'previous_day_close': get_previous_day_close(item.stock_symbol)
            }
        stock_aggregation[item.stock_symbol]['quantity'] += item.quantity
        stock_aggregation[item.stock_symbol]['total_buy_price'] += item.buy_price * item.quantity

    for stock_symbol, values in stock_aggregation.items():
        avg_buy_price = values['total_buy_price'] / values['quantity']
        current_price = values['current_price']
        previous_day_close = values['previous_day_close']
        value = values['quantity'] * current_price
        total_invested += values['quantity'] * avg_buy_price
        total_current_value += value

        day_return = (current_price - previous_day_close) * values['quantity'] if previous_day_close else 0
        total_day_return += day_return

        portfolio_data.append({
            'stock_symbol': stock_symbol,
            'quantity': values['quantity'],
            'buy_price': avg_buy_price,
            'current_price': current_price,
            'value': value,
            'day_return': day_return
        })

    total_returns = total_current_value - total_invested
    percent_gain = (total_returns / total_invested) * 100 if total_invested != 0 else 0

    return jsonify({
        'portfolio': portfolio_data,
        'total_invested': total_invested,
        'total_current_value': total_current_value,
        'total_returns': total_returns,
        'percent_gain': percent_gain,
        'total_day_return': total_day_return
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)
