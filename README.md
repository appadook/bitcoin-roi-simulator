# Bitcoin Investment Analyzer

A comprehensive Python tool to analyze Bitcoin investment strategies using historical data. This tool helps you understand how daily investments in Bitcoin would have performed over different time periods with both numerical analysis and graphical visualization.

## Features

- **Modular Design**: Clean class-based structure with separate methods for different functionalities
- **Flexible Investment Analysis**: Analyze daily investment strategies with customizable parameters
- **Multiple Time Period Options**: Specify investment periods by days, date ranges, or default to all available data
- **Graphical Visualization**: Generate comprehensive charts showing portfolio growth, returns, and Bitcoin price trends
- **Numerical Analysis**: Get detailed numerical summaries of investment performance
- **Smart Price Handling**: Automatically uses Adjusted Close prices when available for more accurate calculations

## Installation

### Quick Setup (Recommended)
```bash
python setup.py
```
This will install dependencies, download data, and run a demo.

### Manual Setup
1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Get Bitcoin historical data (choose one):
   - **Automatic**: Run `python data_downloader.py` and choose option 1 (Yahoo Finance)
   - **Manual**: Download CSV with columns: Date, Open, High, Low, Close, Volume
   - **Sample**: Use the test data generator in `test_analyzer.py`

## Quick Start

```python
from bitcoin_investment_analyzer import BitcoinInvestmentAnalyzer

# Initialize analyzer (automatically loads BTC-daily-prices.csv)
analyzer = BitcoinInvestmentAnalyzer()

# Simulate investing $10 daily for 365 days
results = analyzer.simulate_daily_investment(daily_amount=10, days=365)

# Get numerical summary
analyzer.print_summary()

# Generate graphs
analyzer.plot_investment_growth()
```

## Usage Examples

### Example 1: Fixed Number of Days
```python
# Invest $25 daily for 180 days starting from the first available date
analyzer.simulate_daily_investment(daily_amount=25, days=180)
analyzer.print_summary()
```

### Example 2: Specific Date Range
```python
# Invest $50 daily from January to December 2023
analyzer.simulate_daily_investment(
    daily_amount=50,
    start_date='2023-01-01',
    end_date='2023-12-31'
)
analyzer.plot_investment_growth()
```

### Example 3: Until Present (Default)
```python
# Invest $15 daily from a specific date until the last available data
analyzer.simulate_daily_investment(
    daily_amount=15,
    start_date='2022-06-01'
)
summary = analyzer.get_investment_summary()
print(f"Total return: {summary['return_percentage']:.2f}%")
```

## Class Methods

### Core Methods
- `load_data(file_path)`: Load Bitcoin data from CSV
- `simulate_daily_investment()`: Run investment simulation with flexible parameters
- `get_investment_summary()`: Get numerical results as dictionary
- `print_summary()`: Print formatted investment summary
- `plot_investment_growth()`: Generate comprehensive visualization

### Method Parameters
- `daily_amount`: Amount to invest daily (USD)
- `start_date`: Start date (string or datetime, optional)
- `end_date`: End date (string or datetime, optional)  
- `days`: Number of days to invest (alternative to end_date)

## Data Format

Your CSV should include these columns (case-insensitive):
- Date/date/timestamp
- Open/open
- High/high  
- Low/low
- Close/close
- Volume/volume

## Sample Output

```
==================================================
BITCOIN INVESTMENT ANALYSIS SUMMARY
==================================================
Investment Period: 2023-01-01 to 2023-12-31
Total Days: 365

Investment Details:
  Total Invested: $3,650.00
  Bitcoin Acquired: 0.123456 BTC
  Average BTC Price: $29,567.89

Final Results:
  Portfolio Value: $4,234.56
  Total Return: $584.56
  Return Percentage: 16.02%
  Final BTC Price: $34,321.00
==================================================
```

## Getting Bitcoin Data

### Option 1: Yahoo Finance (Manual)
1. Go to Yahoo Finance Bitcoin page
2. Download historical data as CSV
3. Save as `bitcoin_data.csv`

### Option 2: Kaggle API
```python
from bitcoin_investment_analyzer import download_sample_data
download_sample_data()  # Requires Kaggle API setup
```

### Option 3: Custom Data Source
Any CSV with OHLCV data will work - just ensure proper column names.

## Visualization

The tool generates a 2x2 subplot showing:
1. Portfolio Value vs Total Investment
2. Return Percentage Over Time  
3. Bitcoin Price During Investment Period
4. Cumulative Bitcoin Holdings

## Tips

- Start with small amounts to understand the tool
- Compare different time periods to see market impact
- Use the numerical summary for precise calculations
- Save plots using the `save_path` parameter in `plot_investment_growth()`

## Project Files

- `bitcoin_investment_analyzer.py` - Main analyzer class with all core functionality
- `example_usage.py` - Practical examples and usage demonstrations
- `data_downloader.py` - Utility to download Bitcoin data from multiple sources
- `test_analyzer.py` - Comprehensive testing suite and sample data generator
- `setup.py` - One-click setup script for easy installation
- `requirements.txt` - All required Python packages

## Data Sources

The `data_downloader.py` supports multiple data sources:

1. **Yahoo Finance** (Recommended - Free & Reliable)
   - Up to 10+ years of data
   - No API key required
   - Includes volume data

2. **CoinGecko** (Free, Limited)
   - Up to 365 days for free API
   - No API key required
   - No volume data in OHLC endpoint

3. **CoinAPI** (Requires API Key)
   - Extensive historical data
   - Professional-grade data
   - Requires paid subscription

4. **Sample Data Generator**
   - Creates realistic test data
   - Perfect for development and testing
   - Configurable time periods

## Testing & Development

Run the comprehensive test suite:
```bash
python test_analyzer.py
```

Options available:
1. Basic functionality tests
2. Investment strategy comparisons
3. Full feature demonstration
4. Sample data generation
5. Run all tests

## Advanced Usage

### Strategy Comparison
```python
# Compare different investment amounts
strategies = [
    {'daily_amount': 5, 'name': 'Conservative'},
    {'daily_amount': 25, 'name': 'Moderate'},
    {'daily_amount': 100, 'name': 'Aggressive'}
]

for strategy in strategies:
    analyzer.simulate_daily_investment(daily_amount=strategy['daily_amount'], days=365)
    summary = analyzer.get_investment_summary()
    print(f"{strategy['name']}: {summary['return_percentage']:.2f}% return")
```

### Custom Analysis
```python
# Get raw investment data for custom analysis
results = analyzer.simulate_daily_investment(daily_amount=20, days=180)

# Access detailed daily data
print(results[['Date', 'BTC_Purchased', 'Portfolio_Value', 'Return_Percentage']].head())

# Calculate additional metrics
max_drawdown = results['Return_Percentage'].min()
best_day = results.loc[results['Return_Percentage'].idxmax()]
```

### Save Visualizations
```python
# Save charts to files
analyzer.plot_investment_growth(
    figsize=(15, 10),
    save_path='my_bitcoin_analysis.png'
)
```

## Requirements

- Python 3.7+
- pandas>=1.5.0
- matplotlib>=3.5.0  
- seaborn>=0.11.0
- numpy>=1.21.0
- requests>=2.28.0
- yfinance>=0.2.0 (for Yahoo Finance data)
- kaggle>=1.5.0 (optional, for Kaggle datasets)