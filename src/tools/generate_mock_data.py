import json
import random
from datetime import datetime, timedelta
import os
import yfinance as yf


def generate_insider_trades(ticker: str, num_trades: int = 10) -> list:
    """生成模拟的内部交易数据"""
    trades = []

    # 获取实际的股票价格作为参考
    stock = yf.Ticker(ticker)
    try:
        current_price = stock.info.get(
            'regularMarketPrice', 100)  # 如果获取失败，使用100作为默认值
    except:
        current_price = 100

    # 使用实际股价的±20%范围生成合理的交易价格
    min_price = current_price * 0.8
    max_price = current_price * 1.2

    for _ in range(num_trades):
        # 生成基本交易信息
        is_buy = random.choice([True, False])
        shares = random.randint(1000, 50000)  # 更真实的交易规模
        price = round(random.uniform(min_price, max_price), 2)
        trade_date = datetime.now() - timedelta(days=random.randint(1, 30))

        trades.append({
            "transaction_shares": shares if is_buy else -shares,
            "transaction_type": "BUY" if is_buy else "SELL",
            "value": round(shares * price if is_buy else -shares * price, 2),
            "date": trade_date.strftime("%Y-%m-%d")
        })

    return sorted(trades, key=lambda x: x["date"], reverse=True)


def generate_mock_data(tickers: list):
    """为指定的股票生成模拟数据"""
    print("Generating mock insider trading data...")

    # 生成内部交易数据
    insider_trades = {}
    for ticker in tickers:
        print(f"Processing {ticker}...")
        insider_trades[ticker] = generate_insider_trades(ticker)

    # 确保数据目录存在
    os.makedirs('src/data', exist_ok=True)

    # 保存内部交易数据
    with open('src/data/mock_insider_trades.json', 'w') as f:
        json.dump(insider_trades, f, indent=2)

    print("Mock data generation completed!")


if __name__ == "__main__":
    # 测试数据生成
    tickers = ["AAPL", "MSFT", "GOOGL"]
    generate_mock_data(tickers)
