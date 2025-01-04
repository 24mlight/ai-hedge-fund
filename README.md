# AI Hedge Fund

This is a proof concept for an AI-powered hedge fund. The goal of this project is to explore the use of AI to make trading decisions. This project is for **educational** purposes only and is not intended for real trading or investment.

This system employs several agents working together:

1. Market Data Analyst - Gathers and preprocesses market data
2. Valuation Agent - Calculates the intrinsic value of a stock and generates trading signals
3. Sentiment Agent - Analyzes market sentiment and generates trading signals
4. Fundamentals Agent - Analyzes fundamental data and generates trading signals
5. Technical Analyst - Analyzes technical indicators and generates trading signals
6. Risk Manager - Calculates risk metrics and sets position limits
7. Portfolio Manager - Makes final trading decisions and generates orders

![Screenshot 2024-12-27 at 5 49 56 PM](https://github.com/user-attachments/assets/c281b8c3-d8e6-431e-a05e-d309d306e967)

Note: the system simulates trading decisions, it does not actually trade.

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No warranties or guarantees provided
- Past performance does not indicate future results
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions

By using this software, you agree to use it solely for learning purposes.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Setup

Clone the repository:

```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:

```bash
poetry install
```

3. Set up your environment variables:

```bash
# Create .env file for your API keys
cp .env.example .env

export OPENAI_API_KEY='your-api-key-here' # Get a key from https://platform.openai.com/
export FINANCIAL_DATASETS_API_KEY='your-api-key-here' # Get a key from https://financialdatasets.ai/
```

## Usage

### Running the Hedge Fund

```bash
poetry run python src/main.py --ticker AAPL
```

You can also specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
poetry run python src/main.py --ticker AAPL --show-reasoning
```

You can optionally specify the start and end dates to make decisions for a specific time period.

```bash
poetry run python src/main.py --ticker AAPL --start-date 2024-01-01 --end-date 2024-03-01
```

### Running the Backtester

```bash
poetry run python src/backtester.py --ticker AAPL
```

**Example Output:**

```
Starting backtest...
Date         Ticker Action Quantity    Price         Cash    Stock  Total Value
----------------------------------------------------------------------
2024-01-01   AAPL   buy       519.0   192.53        76.93    519.0    100000.00
2024-01-02   AAPL   hold          0   185.64        76.93    519.0     96424.09
2024-01-03   AAPL   hold          0   184.25        76.93    519.0     95702.68
2024-01-04   AAPL   hold          0   181.91        76.93    519.0     94488.22
2024-01-05   AAPL   hold          0   181.18        76.93    519.0     94109.35
2024-01-08   AAPL   sell        519   185.56     96382.57      0.0     96382.57
2024-01-09   AAPL   buy       520.0   185.14       109.77    520.0     96382.57
```

You can optionally specify the start and end dates to backtest over a specific time period.

```bash
poetry run python src/backtester.py --ticker AAPL --start-date 2024-01-01 --end-date 2024-03-01
```

## Project Structure

```
ai-hedge-fund/
├── src/
│   ├── agents/                   # Agent definitions and workflow
│   │   ├── fundamentals.py       # Fundamental analysis agent
│   │   ├── market_data.py        # Market data agent
│   │   ├── portfolio_manager.py  # Portfolio management agent
│   │   ├── risk_manager.py       # Risk management agent
│   │   ├── sentiment.py          # Sentiment analysis agent
│   │   ├── state.py              # Agent state
│   │   ├── technicals.py         # Technical analysis agent
│   │   ├── valuation.py          # Valuation analysis agent
│   ├── tools/                    # Agent tools
│   │   ├── api.py                # API tools
│   ├── backtester.py             # Backtesting tools
│   ├── main.py # Main entry point
├── pyproject.toml
├── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 项目详细说明

### 架构设计

本项目是一个基于多智能体（Multi-Agent）的 AI 对冲基金系统，采用模块化设计，每个代理（Agent）都有其专门的职责。系统的架构如下：

```
Market Data Analyst → [Technical/Fundamentals/Sentiment/Valuation Analyst] → Risk Manager → Portfolio Manager → Trading Decision
```

#### 代理角色和职责

1. **Market Data Analyst（市场数据分析师）**

   - 作为系统的入口点
   - 负责收集和预处理所有必要的市场数据
   - 将处理后的数据分发给其他分析师
   - 数据来源：yfinance API 和模拟数据

2. **Technical Analyst（技术分析师）**

   - 分析价格趋势、成交量、动量等技术指标
   - 生成基于技术分析的交易信号
   - 关注短期市场走势和交易机会

3. **Fundamentals Analyst（基本面分析师）**

   - 分析公司财务指标和经营状况
   - 评估公司的长期发展潜力
   - 生成基于基本面的交易信号

4. **Sentiment Analyst（情绪分析师）**

   - 分析内部交易数据
   - 评估市场情绪和内部人士行为
   - 生成基于情绪的交易信号

5. **Valuation Analyst（估值分析师）**

   - 进行公司估值分析
   - 评估股票的内在价值
   - 生成基于估值的交易信号

6. **Risk Manager（风险管理员）**

   - 整合所有分析师的交易信号
   - 评估潜在风险
   - 设定交易限制和风险控制参数
   - 生成风险管理信号

7. **Portfolio Manager（投资组合管理员）**
   - 作为最终决策者
   - 综合考虑所有信号和风险因素
   - 做出最终的交易决策（买入/卖出/持有）
   - 确保决策符合风险管理要求

### 数据流和处理

#### 数据类型

1. **市场价格数据**

   ```python
   {
       "date": "YYYY-MM-DD",
       "open": float,
       "high": float,
       "low": float,
       "close": float,
       "volume": int
   }
   ```

2. **财务指标数据**

   ```python
   {
       "market_cap": float,
       "pe_ratio": float,
       "price_to_book": float,
       "dividend_yield": float,
       "revenue": float,
       "net_income": float,
       # ... 更多财务指标
   }
   ```

3. **财务项目数据**

   ```python
   {
       "free_cash_flow": float,
       "net_income": float,
       "depreciation_and_amortization": float,
       "capital_expenditure": float,
       "working_capital": float
   }
   ```

4. **内部交易数据**
   ```python
   {
       "transaction_shares": int,  # 正数表示买入，负数表示卖出
       "transaction_type": str,    # "BUY" 或 "SELL"
       "value": float,            # 交易总价值
       "date": "YYYY-MM-DD"       # 交易日期
   }
   ```

#### 数据流转过程

1. **数据采集阶段**

   - Market Data Analyst 从 yfinance 获取实时市场数据
   - 对于无法获取的数据（如内部交易），使用模拟数据
   - 数据经过预处理和格式化

2. **分析阶段**

   - 四个专业分析师并行工作
   - 每个分析师根据自己的专业领域分析数据
   - 生成相应的交易信号

3. **风险评估阶段**

   - Risk Manager 接收并整合所有分析信号
   - 评估潜在风险和收益
   - 设定交易限制

4. **决策阶段**
   - Portfolio Manager 接收风险管理信号
   - 综合评估所有信息
   - 做出最终交易决策

### 代理协作机制

1. **信息共享**

   - 所有代理共享同一个状态对象（AgentState）
   - 通过消息传递机制进行通信
   - 每个代理都可以访问必要的历史数据

2. **决策权重**
   Portfolio Manager 在做决策时考虑不同信号的权重：

   - 估值分析：35%
   - 基本面分析：30%
   - 技术分析：25%
   - 情绪分析：10%

3. **风险控制**
   - 强制性风险限制
   - 最大持仓限制
   - 交易规模限制
   - 止损和止盈设置

### 系统特点

1. **模块化设计**

   - 每个代理都是独立的模块
   - 易于维护和升级
   - 可以单独测试和优化

2. **可扩展性**

   - 可以轻松添加新的分析师
   - 支持添加新的数据源
   - 可以扩展决策策略

3. **风险管理**

   - 多层次的风险控制
   - 实时风险评估
   - 自动止损机制

4. **智能决策**
   - 基于多维度分析
   - 考虑多个市场因素
   - 动态调整策略

### 使用示例

```bash
# 运行交易决策（以 AAPL 为例）
poetry run python src/main.py --ticker AAPL --show-reasoning

# 生成模拟数据
poetry run python src/tools/generate_mock_data.py
```

### 未来展望

1. **数据源扩展**

   - 添加更多实时数据源
   - 接入真实的内部交易数据
   - 增加市场新闻和社交媒体数据

2. **功能增强**

   - 添加更多技术指标
   - 实现自动化回测
   - 支持多股票组合管理

3. **性能优化**
   - 提高数据处理效率
   - 优化决策算法
   - 增加并行处理能力
