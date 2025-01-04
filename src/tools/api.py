from typing import Dict, Any, List
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import random
import json


def get_financial_metrics(ticker: str) -> Dict[str, Any]:
    """获取财务指标数据"""
    stock = yf.Ticker(ticker)
    info = stock.info

    try:
        financials = stock.financials.iloc[:, 0]  # 获取最新的财务数据
        # 计算增长率
        if len(stock.financials.columns) > 1:
            prev_financials = stock.financials.iloc[:, 1]
            revenue_growth = (financials.get("Total Revenue", 0) - prev_financials.get(
                "Total Revenue", 0)) / prev_financials.get("Total Revenue", 1)
            earnings_growth = (financials.get("Net Income", 0) - prev_financials.get(
                "Net Income", 0)) / prev_financials.get("Net Income", 1)
        else:
            revenue_growth = 0
            earnings_growth = 0
    except:
        financials = pd.Series()
        revenue_growth = 0
        earnings_growth = 0

    # 构建与项目需求一致的指标数据
    metrics = {
        "market_cap": info.get("marketCap", 0),
        "pe_ratio": info.get("forwardPE", 0),
        "price_to_book": info.get("priceToBook", 0),
        "dividend_yield": info.get("dividendYield", 0),
        "revenue": financials.get("Total Revenue", 0),
        "net_income": financials.get("Net Income", 0),
        "return_on_equity": info.get("returnOnEquity", 0),
        "net_margin": info.get("profitMargins", 0),
        "operating_margin": info.get("operatingMargins", 0),
        "revenue_growth": revenue_growth,
        "earnings_growth": earnings_growth,
        "book_value_growth": 0,  # yfinance 不提供这个数据，需要模拟
        "current_ratio": info.get("currentRatio", 0),
        "debt_to_equity": info.get("debtToEquity", 0),
        "free_cash_flow_per_share": info.get("freeCashflow", 0) / info.get("sharesOutstanding", 1) if info.get("sharesOutstanding", 0) > 0 else 0,
        "earnings_per_share": info.get("trailingEps", 0),
        "price_to_earnings_ratio": info.get("forwardPE", 0),
        "price_to_book_ratio": info.get("priceToBook", 0),
        "price_to_sales_ratio": info.get("priceToSalesTrailing12Months", 0)
    }

    return [metrics]  # 返回列表以符合项目需求


def get_financial_statements(ticker: str) -> Dict[str, Any]:
    """获取财务报表数据"""
    stock = yf.Ticker(ticker)

    try:
        financials = stock.financials  # 获取所有财务数据
        cash_flow = stock.cashflow     # 获取所有现金流数据
        balance = stock.balance_sheet  # 获取所有资产负债表数据

        # 准备最近两个季度的数据
        line_items = []
        for i in range(min(2, len(financials.columns))):
            current_financials = financials.iloc[:, i]
            current_cash_flow = cash_flow.iloc[:, i]
            current_balance = balance.iloc[:, i]

            line_item = {
                "free_cash_flow": current_cash_flow.get("Free Cash Flow", 0),
                "net_income": current_financials.get("Net Income", 0),
                "depreciation_and_amortization": current_cash_flow.get("Depreciation", 0),
                "capital_expenditure": current_cash_flow.get("Capital Expenditure", 0),
                "working_capital": (
                    current_balance.get("Total Current Assets", 0) -
                    current_balance.get("Total Current Liabilities", 0)
                )
            }
            line_items.append(line_item)

        # 如果只有一个季度的数据，复制一份作为前一季度
        if len(line_items) == 1:
            line_items.append(line_items[0])

        return line_items

    except Exception as e:
        print(f"Warning: Error getting financial statements: {e}")
        # 返回两个相同的默认数据
        default_item = {
            "free_cash_flow": 0,
            "net_income": 0,
            "depreciation_and_amortization": 0,
            "capital_expenditure": 0,
            "working_capital": 0
        }
        return [default_item, default_item]


def get_insider_trades(ticker: str) -> List[Dict[str, Any]]:
    """从数据文件获取内部交易数据"""
    try:
        with open('src/data/mock_insider_trades.json', 'r') as f:
            all_trades = json.load(f)
        return all_trades.get(ticker, [])
    except FileNotFoundError:
        print("Warning: Mock data file not found. Generating random data...")
        # 如果文件不存在，返回随机数据作为后备
        num_trades = random.randint(5, 10)
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
            is_buy = random.choice([True, False])
            # 与 generate_mock_data.py 保持一致
            shares = random.randint(1000, 50000)
            price = round(random.uniform(min_price, max_price), 2)

            trades.append({
                "transaction_shares": shares if is_buy else -shares,
                "transaction_type": "BUY" if is_buy else "SELL",
                # 添加 round 保持精度一致
                "value": round(shares * price if is_buy else -shares * price, 2),
                "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            })

        return sorted(trades, key=lambda x: x["date"], reverse=True)


def get_market_data(ticker: str) -> Dict[str, Any]:
    """获取市场数据"""
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "market_cap": info.get("marketCap", 0),
        "volume": info.get("volume", 0),
        "average_volume": info.get("averageVolume", 0),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0)
    }


def get_price_history(ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """获取历史价格数据"""
    stock = yf.Ticker(ticker)

    # 如果没有提供日期，默认获取过去3个月的数据
    if not end_date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if not start_date:
        start_date = end_date - timedelta(days=90)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # 获取历史数据
    df = stock.history(start=start_date, end=end_date)

    # 确保数据格式统一
    if not df.empty:
        # 保持日期作为索引，但格式化为字符串
        df.index = pd.to_datetime(df.index).strftime("%Y-%m-%d")
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

    return df


def prices_to_df(prices: list) -> pd.DataFrame:
    """将价格列表转换为 DataFrame"""
    if isinstance(prices, pd.DataFrame):
        return prices  # 如果已经是 DataFrame，直接返回
    df = pd.DataFrame(prices)
    return df
