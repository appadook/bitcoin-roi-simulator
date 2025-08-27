import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from typing import Optional, Union
import os


class BitcoinInvestmentAnalyzer:
    """
    A class to analyze Bitcoin investment strategies using historical data.
    Supports daily investment analysis with graphical and numerical outputs.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the analyzer with Bitcoin data.
        
        Args:
            data_path: Path to CSV file with Bitcoin data. If None, will look for default files.
        """
        self.data = None
        self.investment_history = None
        
        if data_path:
            self.load_data(data_path)
        else:
            self._try_load_default_data()
    
    def _try_load_default_data(self):
        """Try to load data from common default file names."""
        possible_files = [
            'BTC-daily-prices.csv',
            'BTC-USD.csv',
            'bitcoin_historical.csv',
            'btc_data.csv'
        ]
        
        for file in possible_files:
            if os.path.exists(file):
                print(f"Found data file: {file}")
                self.load_data(file)
                break
        else:
            print("No default data file found. Please provide data_path or download data first.")
    
    def load_data(self, file_path: str):
        """
        Load Bitcoin historical data from CSV file.
        Expected columns: Date, Open, High, Low, Close, Adj Close, Volume
        
        Args:
            file_path: Path to the CSV file containing Bitcoin data
        """
        try:
            self.data = pd.read_csv(file_path)
            
            # Convert Date column to datetime
            if 'Date' in self.data.columns:
                self.data['Date'] = pd.to_datetime(self.data['Date'])
                self.data = self.data.sort_values('Date').reset_index(drop=True)
            else:
                raise ValueError("Date column not found in the CSV file")
            
            # Verify required columns exist
            required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Use Adj Close if available, otherwise use Close for calculations
            if 'Adj Close' in self.data.columns:
                self.data['Price'] = self.data['Adj Close']
                print("Using Adj Close for price calculations")
            else:
                self.data['Price'] = self.data['Close']
                print("Using Close for price calculations")
            
            print(f"Data loaded successfully: {len(self.data)} records")
            print(f"Date range: {self.data['Date'].min().strftime('%Y-%m-%d')} to {self.data['Date'].max().strftime('%Y-%m-%d')}")
            print(f"Columns available: {list(self.data.columns)}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = None
    
    def simulate_daily_investment(self, 
                                daily_amount: float,
                                start_date: Optional[Union[str, datetime]] = None,
                                end_date: Optional[Union[str, datetime]] = None,
                                days: Optional[int] = None) -> pd.DataFrame:
        """
        Simulate daily investment strategy.
        
        Args:
            daily_amount: Amount to invest daily (in USD)
            start_date: Start date for investment (if None, uses first available date)
            end_date: End date for investment (if None, uses last available date or calculated from days)
            days: Number of days to invest (alternative to end_date)
            
        Returns:
            DataFrame with investment history
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        # Handle date parameters
        if start_date is None:
            start_date = self.data['Date'].min()
        elif isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        
        if days is not None:
            end_date = start_date + timedelta(days=days)
        elif end_date is None:
            end_date = self.data['Date'].max()
        elif isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        # Filter data for the investment period
        mask = (self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)
        investment_data = self.data[mask].copy()
        
        if investment_data.empty:
            raise ValueError("No data available for the specified date range.")
        
        # Calculate investment metrics using Price column (Adj Close if available, otherwise Close)
        investment_data['Daily_Investment'] = daily_amount
        investment_data['BTC_Purchased'] = daily_amount / investment_data['Price']
        investment_data['Cumulative_Investment'] = investment_data['Daily_Investment'].cumsum()
        investment_data['Cumulative_BTC'] = investment_data['BTC_Purchased'].cumsum()
        investment_data['Portfolio_Value'] = investment_data['Cumulative_BTC'] * investment_data['Price']
        investment_data['Total_Return'] = investment_data['Portfolio_Value'] - investment_data['Cumulative_Investment']
        investment_data['Return_Percentage'] = (investment_data['Total_Return'] / investment_data['Cumulative_Investment']) * 100
        
        self.investment_history = investment_data
        return investment_data
    
    def get_investment_summary(self) -> dict:
        """
        Get numerical summary of the investment performance.
        
        Returns:
            Dictionary with key investment metrics
        """
        if self.investment_history is None:
            raise ValueError("No investment simulation run. Please run simulate_daily_investment first.")
        
        final_row = self.investment_history.iloc[-1]
        
        summary = {
            'total_invested': final_row['Cumulative_Investment'],
            'total_btc_acquired': final_row['Cumulative_BTC'],
            'final_portfolio_value': final_row['Portfolio_Value'],
            'total_return': final_row['Total_Return'],
            'return_percentage': final_row['Return_Percentage'],
            'investment_days': len(self.investment_history),
            'average_btc_price': final_row['Cumulative_Investment'] / final_row['Cumulative_BTC'],
            'final_btc_price': final_row['Price'],
            'start_date': self.investment_history['Date'].min(),
            'end_date': self.investment_history['Date'].max()
        }
        
        return summary
    
    def plot_investment_growth(self, figsize: tuple = (12, 8), save_path: Optional[str] = None):
        """
        Create graphical representation of investment growth.
        
        Args:
            figsize: Figure size for the plot
            save_path: Path to save the plot (if None, displays only)
        """
        if self.investment_history is None:
            raise ValueError("No investment simulation run. Please run simulate_daily_investment first.")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Bitcoin Daily Investment Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Portfolio Value vs Investment
        ax1.plot(self.investment_history['Date'], self.investment_history['Cumulative_Investment'], 
                label='Total Invested', color='blue', linewidth=2)
        ax1.plot(self.investment_history['Date'], self.investment_history['Portfolio_Value'], 
                label='Portfolio Value', color='green', linewidth=2)
        ax1.set_title('Portfolio Value vs Total Investment')
        ax1.set_ylabel('Value (USD)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Return Percentage
        ax2.plot(self.investment_history['Date'], self.investment_history['Return_Percentage'], 
                color='orange', linewidth=2)
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        ax2.set_title('Return Percentage Over Time')
        ax2.set_ylabel('Return (%)')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Bitcoin Price
        ax3.plot(self.investment_history['Date'], self.investment_history['Price'], 
                color='purple', linewidth=2)
        ax3.set_title('Bitcoin Price Over Investment Period')
        ax3.set_ylabel('BTC Price (USD)')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Cumulative BTC Holdings
        ax4.plot(self.investment_history['Date'], self.investment_history['Cumulative_BTC'], 
                color='red', linewidth=2)
        ax4.set_title('Cumulative Bitcoin Holdings')
        ax4.set_ylabel('BTC Amount')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        plt.show()
    
    def print_summary(self):
        """Print a formatted summary of the investment analysis."""
        summary = self.get_investment_summary()
        
        print("\n" + "="*50)
        print("BITCOIN INVESTMENT ANALYSIS SUMMARY")
        print("="*50)
        print(f"Investment Period: {summary['start_date'].strftime('%Y-%m-%d')} to {summary['end_date'].strftime('%Y-%m-%d')}")
        print(f"Total Days: {summary['investment_days']}")
        print(f"\nInvestment Details:")
        print(f"  Total Invested: ${summary['total_invested']:,.2f}")
        print(f"  Bitcoin Acquired: {summary['total_btc_acquired']:.6f} BTC")
        print(f"  Average BTC Price: ${summary['average_btc_price']:,.2f}")
        print(f"\nFinal Results:")
        print(f"  Portfolio Value: ${summary['final_portfolio_value']:,.2f}")
        print(f"  Total Return: ${summary['total_return']:,.2f}")
        print(f"  Return Percentage: {summary['return_percentage']:.2f}%")
        print(f"  Final BTC Price: ${summary['final_btc_price']:,.2f}")
        print("="*50)


# Example usage and helper functions
def download_sample_data():
    """
    Helper function to download sample Bitcoin data.
    Note: You'll need to set up Kaggle API credentials for this to work.
    """
    try:
        import kaggle
        print("Downloading Bitcoin data from Kaggle...")
        # This is an example - you'll need to find the actual dataset name
        kaggle.api.dataset_download_files('mczielinski/bitcoin-historical-data', 
                                         path='.', unzip=True)
        print("Data downloaded successfully!")
    except Exception as e:
        print(f"Error downloading data: {e}")
        print("Please manually download Bitcoin historical data CSV file.")


if __name__ == "__main__":
    # Example usage
    analyzer = BitcoinInvestmentAnalyzer()
    
    # If no data is loaded, show instructions
    if analyzer.data is None:
        print("\nTo use this analyzer, you need Bitcoin historical data.")
        print("You can:")
        print("1. Download data manually and save as 'bitcoin_data.csv'")
        print("2. Use the download_sample_data() function (requires Kaggle setup)")
        print("3. Provide your own CSV file path when creating the analyzer")