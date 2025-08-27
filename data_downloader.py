#!/usr/bin/env python3
"""
Data downloader utility for Bitcoin Investment Analyzer
Supports multiple data sources for Bitcoin historical data
"""

import pandas as pd
import requests
from datetime import datetime, timedelta
import os
from typing import Optional


class BitcoinDataDownloader:
    """Download Bitcoin historical data from various sources."""
    
    def __init__(self):
        self.data = None
    
    def download_yahoo_finance(self, 
                              symbol: str = 'BTC-USD',
                              period: str = '2y',
                              save_path: str = 'bitcoin_data.csv') -> bool:
        """
        Download Bitcoin data from Yahoo Finance using yfinance.
        
        Args:
            symbol: Trading symbol (default: BTC-USD)
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            save_path: Path to save the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import yfinance as yf
            print(f"Downloading {symbol} data for period: {period}")
            
            # Download data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                print("No data received from Yahoo Finance")
                return False
            
            # Reset index to get Date as column
            data.reset_index(inplace=True)
            
            # Standardize column names
            data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
            
            # Keep only OHLCV columns
            data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Save to CSV
            data.to_csv(save_path, index=False)
            print(f"Data saved to {save_path}")
            print(f"Records: {len(data)}")
            print(f"Date range: {data['Date'].min()} to {data['Date'].max()}")
            
            self.data = data
            return True
            
        except ImportError:
            print("yfinance not installed. Install with: pip install yfinance")
            return False
        except Exception as e:
            print(f"Error downloading from Yahoo Finance: {e}")
            return False
    
    def download_coinapi(self, 
                        api_key: str,
                        symbol: str = 'BITSTAMP_SPOT_BTC_USD',
                        days: int = 365,
                        save_path: str = 'bitcoin_data.csv') -> bool:
        """
        Download Bitcoin data from CoinAPI.
        
        Args:
            api_key: Your CoinAPI key
            symbol: Trading symbol
            days: Number of days of historical data
            save_path: Path to save the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            url = f"https://rest.coinapi.io/v1/ohlcv/{symbol}/history"
            headers = {'X-CoinAPI-Key': api_key}
            params = {
                'period_id': '1DAY',
                'time_start': start_date.isoformat(),
                'time_end': end_date.isoformat()
            }
            
            print(f"Downloading {symbol} data from CoinAPI...")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"API request failed: {response.status_code}")
                return False
            
            data = response.json()
            
            if not data:
                print("No data received from CoinAPI")
                return False
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            df['Date'] = pd.to_datetime(df['time_period_start']).dt.date
            df = df.rename(columns={
                'price_open': 'Open',
                'price_high': 'High', 
                'price_low': 'Low',
                'price_close': 'Close',
                'volume_traded': 'Volume'
            })
            
            # Keep only required columns
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df = df.sort_values('Date').reset_index(drop=True)
            
            # Save to CSV
            df.to_csv(save_path, index=False)
            print(f"Data saved to {save_path}")
            print(f"Records: {len(df)}")
            
            self.data = df
            return True
            
        except Exception as e:
            print(f"Error downloading from CoinAPI: {e}")
            return False
    
    def download_coingecko(self, 
                          coin_id: str = 'bitcoin',
                          vs_currency: str = 'usd',
                          days: int = 365,
                          save_path: str = 'bitcoin_data.csv') -> bool:
        """
        Download Bitcoin data from CoinGecko (free API).
        
        Args:
            coin_id: Coin identifier (default: bitcoin)
            vs_currency: Currency to price against (default: usd)
            days: Number of days (max 365 for free API)
            save_path: Path to save the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
            params = {
                'vs_currency': vs_currency,
                'days': min(days, 365)  # Free API limit
            }
            
            print(f"Downloading {coin_id} data from CoinGecko...")
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                print(f"API request failed: {response.status_code}")
                return False
            
            data = response.json()
            
            if not data:
                print("No data received from CoinGecko")
                return False
            
            # Convert to DataFrame
            df_data = []
            for item in data:
                timestamp, open_price, high, low, close = item
                date = datetime.fromtimestamp(timestamp / 1000).date()
                df_data.append({
                    'Date': date,
                    'Open': open_price,
                    'High': high,
                    'Low': low,
                    'Close': close,
                    'Volume': 0  # CoinGecko OHLC doesn't include volume
                })
            
            df = pd.DataFrame(df_data)
            df = df.sort_values('Date').reset_index(drop=True)
            
            # Save to CSV
            df.to_csv(save_path, index=False)
            print(f"Data saved to {save_path}")
            print(f"Records: {len(df)}")
            print("Note: Volume data not available from CoinGecko OHLC endpoint")
            
            self.data = df
            return True
            
        except Exception as e:
            print(f"Error downloading from CoinGecko: {e}")
            return False
    
    def create_sample_data(self, 
                          days: int = 365,
                          save_path: str = 'bitcoin_data.csv') -> bool:
        """
        Create realistic sample Bitcoin data for testing.
        
        Args:
            days: Number of days to generate
            save_path: Path to save the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import numpy as np
            
            print(f"Creating sample Bitcoin data for {days} days...")
            
            # Generate dates
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Generate realistic price data using geometric Brownian motion
            np.random.seed(42)  # For reproducible results
            initial_price = 35000
            
            # Parameters for realistic Bitcoin volatility
            drift = 0.0005  # Small positive drift (about 18% annual)
            volatility = 0.04  # 4% daily volatility
            
            prices = [initial_price]
            for i in range(len(dates) - 1):
                random_shock = np.random.normal(0, 1)
                price_change = drift + volatility * random_shock
                new_price = prices[-1] * np.exp(price_change)
                prices.append(max(new_price, 1000))  # Price floor
            
            # Generate OHLCV data
            data = []
            for i, (date, close) in enumerate(zip(dates, prices)):
                # Generate realistic intraday range
                daily_volatility = np.random.uniform(0.02, 0.08)  # 2-8% daily range
                
                # High and low around close price
                high = close * (1 + daily_volatility * np.random.uniform(0.3, 1.0))
                low = close * (1 - daily_volatility * np.random.uniform(0.3, 1.0))
                
                # Open price within the range
                open_price = low + (high - low) * np.random.uniform(0.2, 0.8)
                
                # Volume with some correlation to price movement
                base_volume = 25000
                volatility_factor = abs(close - open_price) / open_price
                volume = base_volume * (1 + volatility_factor * 10) * np.random.uniform(0.5, 2.0)
                
                data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Open': round(open_price, 2),
                    'High': round(high, 2),
                    'Low': round(low, 2),
                    'Close': round(close, 2),
                    'Volume': round(volume, 2)
                })
            
            # Create DataFrame and save
            df = pd.DataFrame(data)
            df.to_csv(save_path, index=False)
            
            print(f"Sample data saved to {save_path}")
            print(f"Price range: ${df['Low'].min():.2f} - ${df['High'].max():.2f}")
            print(f"Final price: ${df['Close'].iloc[-1]:.2f}")
            
            self.data = df
            return True
            
        except Exception as e:
            print(f"Error creating sample data: {e}")
            return False


def main():
    """Interactive data downloader."""
    downloader = BitcoinDataDownloader()
    
    print("Bitcoin Data Downloader")
    print("="*30)
    print("Choose a data source:")
    print("1. Yahoo Finance (recommended - free, reliable)")
    print("2. CoinGecko (free, limited to 365 days)")
    print("3. CoinAPI (requires API key)")
    print("4. Create sample data (for testing)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        print("\nYahoo Finance Download")
        period = input("Enter period (1y, 2y, 5y, max) [default: 2y]: ").strip() or '2y'
        filename = input("Save as [default: bitcoin_data.csv]: ").strip() or 'bitcoin_data.csv'
        
        success = downloader.download_yahoo_finance(period=period, save_path=filename)
        if success:
            print(f"\n✓ Successfully downloaded Bitcoin data to {filename}")
        else:
            print("\n✗ Download failed. Try installing yfinance: pip install yfinance")
    
    elif choice == '2':
        print("\nCoinGecko Download")
        days = input("Enter number of days [default: 365]: ").strip()
        days = int(days) if days.isdigit() else 365
        filename = input("Save as [default: bitcoin_data.csv]: ").strip() or 'bitcoin_data.csv'
        
        success = downloader.download_coingecko(days=days, save_path=filename)
        if success:
            print(f"\n✓ Successfully downloaded Bitcoin data to {filename}")
        else:
            print("\n✗ Download failed")
    
    elif choice == '3':
        print("\nCoinAPI Download")
        api_key = input("Enter your CoinAPI key: ").strip()
        if not api_key:
            print("API key required for CoinAPI")
            return
        
        days = input("Enter number of days [default: 365]: ").strip()
        days = int(days) if days.isdigit() else 365
        filename = input("Save as [default: bitcoin_data.csv]: ").strip() or 'bitcoin_data.csv'
        
        success = downloader.download_coinapi(api_key=api_key, days=days, save_path=filename)
        if success:
            print(f"\n✓ Successfully downloaded Bitcoin data to {filename}")
        else:
            print("\n✗ Download failed")
    
    elif choice == '4':
        print("\nCreate Sample Data")
        days = input("Enter number of days [default: 365]: ").strip()
        days = int(days) if days.isdigit() else 365
        filename = input("Save as [default: bitcoin_data.csv]: ").strip() or 'bitcoin_data.csv'
        
        success = downloader.create_sample_data(days=days, save_path=filename)
        if success:
            print(f"\n✓ Successfully created sample data: {filename}")
        else:
            print("\n✗ Failed to create sample data")
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()