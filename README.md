# Finding the Starting Point of a Stock Rally

## Overview
This project provides an analytical tool for stock market enthusiasts and traders to visualize and analyze stock price trends. It focuses on identifying potential starting points of stock rallies using indicators like MACD, RSI, and Bollinger Bands.

## Features
- **Stock Data Retrieval**: Fetch daily stock data using Yahoo Finance.
- **MACD Calculation**: Compute the Moving Average Convergence Divergence (MACD) and Signal Line.
- **RSI Calculation**: Calculate the Relative Strength Index (RSI).
- **Bollinger Bands**: Visualize stock price fluctuations with Bollinger Bands.
- **Rising Signal Detection**: Identify points where a stock might be entering a rally phase.
- **Data Visualization**: Generate clear and informative charts with annotations for key signals.

## Requirements
The following Python libraries are required:
- `yfinance`: For fetching stock market data.
- `pandas`: For data manipulation.
- `numpy`: For numerical calculations.
- `matplotlib`: For data visualization.

You can install the dependencies using:
```bash
pip install yfinance pandas numpy matplotlib
```

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/isaac884/Finding-the-starting-point-of-a-stock-rally.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Finding-the-starting-point-of-a-stock-rally
   ```
3. Run the script:
   ```bash
   python stock_rally.py
   ```
4. Enter the stock symbol and desired period when prompted. Example inputs:
   - Stock Symbol: `AAPL`
   - Period: `1y`

## Inputs
- **Stock Symbol**: The ticker symbol of the stock (e.g., `AAPL`, `GOOG`, `MSFT`).
- **Period**: The time range for analysis. Supported values:
  - `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

## Outputs
- Visualizations include:
  1. **Stock Price Chart**: Monthly close prices with identified rising points.
  2. **MACD and Signal Line**: Highlighting crossover points.
  3. **RSI Chart**: Identifying overbought and oversold regions.
  4. **Bollinger Bands**: Showing price deviations.

## Example
**Input:**
```
Enter the stock symbol: AAPL
Enter the period you want, must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'] 
Please enter: 1y
```
**Output:**
- A series of charts showing AAPL's stock price trends, MACD signals, RSI levels, and Bollinger Bands for the past year.

## Contributions
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## Notes
- Ensure your internet connection is active, as the script fetches data from Yahoo Finance.
- The analysis is based on historical data and should not be used for financial advice.

---


## Author
Developed by Isaac.
