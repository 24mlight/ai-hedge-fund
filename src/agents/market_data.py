from langchain_core.messages import HumanMessage
from tools.openrouter_config import get_chat_completion

from agents.state import AgentState
from tools.api import get_financial_metrics, get_financial_statements, get_insider_trades, get_market_data, get_price_history

from datetime import datetime


def market_data_agent(state: AgentState):
    """Responsible for gathering and preprocessing market data"""
    messages = state["messages"]
    data = state["data"]

    # Set default dates
    end_date = data["end_date"] or datetime.now().strftime('%Y-%m-%d')
    if not data["start_date"]:
        # Calculate 3 months before end_date
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = end_date_obj.replace(month=end_date_obj.month - 3) if end_date_obj.month > 3 else \
            end_date_obj.replace(year=end_date_obj.year - 1,
                                 month=end_date_obj.month + 9)
        start_date = start_date.strftime('%Y-%m-%d')
    else:
        start_date = data["start_date"]

    # Get all required data
    ticker = data["ticker"]
    prices_df = get_price_history(ticker, start_date, end_date)
    financial_metrics = get_financial_metrics(ticker)
    financial_line_items = get_financial_statements(ticker)
    insider_trades = get_insider_trades(ticker)
    market_data = get_market_data(ticker)

    return {
        "messages": messages,
        "data": {
            **data,
            "prices": prices_df.to_dict('records'),
            "start_date": start_date,
            "end_date": end_date,
            "financial_metrics": financial_metrics,
            "financial_line_items": financial_line_items,
            "insider_trades": insider_trades,
            "market_cap": market_data["market_cap"],
            "market_data": market_data,
        }
    }
