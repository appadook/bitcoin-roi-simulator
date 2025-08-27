#!/usr/bin/env python3
"""
Interactive Bitcoin Investment Analyzer
Allows user input for all simulation parameters
"""

from bitcoin_investment_analyzer import BitcoinInvestmentAnalyzer
from data_downloader import BitcoinDataDownloader
from datetime import datetime, timedelta
import os
import sys


def get_user_input():
    """Get investment parameters from user input."""
    print("Bitcoin Investment Analyzer - Interactive Mode")
    print("=" * 50)
    
    # Check if data exists
    if not os.path.exists('bitcoin_data.csv'):
        print("No Bitcoin data found. Let's get some data first.")
        download_data()
    
    print("\nEnter your investment parameters:")
    print("-" * 30)
    
    # Get daily investment amount
    while True:
        try:
            daily_amount = float(input("Daily investment amount (USD): $"))
            if daily_amount <= 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Get date range preference
    print("\nChoose your investment period:")
    print("1. Specific date range (start date to end date)")
    print("2. Number of days from start date")
    print("3. Number of days from most recent data")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Please enter 1, 2, or 3.")
    
    start_date = None
    end_date = None
    days = None
    
    if choice == '1':
        # Specific date range
        start_date = get_date_input("Enter start date (YYYY-MM-DD): ")
        end_date = get_date_input("Enter end date (YYYY-MM-DD): ")
        
        if end_date <= start_date:
            print("End date must be after start date. Adjusting...")
            end_date = start_date + timedelta(days=30)
            print(f"Adjusted end date to: {end_date.strftime('%Y-%m-%d')}")
    
    elif choice == '2':
        # Days from start date
        start_date = get_date_input("Enter start date (YYYY-MM-DD): ")
        while True:
            try:
                days = int(input("Number of days to invest: "))
                if days <= 0:
                    print("Please enter a positive number of days.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
    
    elif choice == '3':
        # Days from most recent data
        while True:
            try:
                days = int(input("Number of days to invest (from most recent data): "))
                if days <= 0:
                    print("Please enter a positive number of days.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
    
    return {
        'daily_amount': daily_amount,
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
        'choice': choice
    }


def get_date_input(prompt):
    """Get a valid date from user input."""
    while True:
        date_str = input(prompt).strip()
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj
        except ValueError:
            print("Please enter date in YYYY-MM-DD format (e.g., 2023-01-01)")


def download_data():
    """Download Bitcoin data if not available."""
    print("\nDownloading Bitcoin data...")
    downloader = BitcoinDataDownloader()
    
    # Try Yahoo Finance first
    success = downloader.download_yahoo_finance(period='5y', save_path='bitcoin_data.csv')
    
    if not success:
        print("Yahoo Finance failed, creating sample data...")
        success = downloader.create_sample_data(days=1000, save_path='bitcoin_data.csv')
    
    if success:
        print("✓ Bitcoin data ready")
    else:
        print("✗ Failed to get data. Exiting...")
        sys.exit(1)


def display_data_info(analyzer):
    """Display information about the loaded data."""
    if analyzer.data is not None:
        print(f"\nData Information:")
        print(f"- Records available: {len(analyzer.data):,}")
        print(f"- Date range: {analyzer.data['Date'].min().strftime('%Y-%m-%d')} to {analyzer.data['Date'].max().strftime('%Y-%m-%d')}")
        print(f"- Latest BTC price: ${analyzer.data['Close'].iloc[-1]:,.2f}")
        print(f"- Price range: ${analyzer.data['Close'].min():,.2f} - ${analyzer.data['Close'].max():,.2f}")


def run_simulation(params):
    """Run the investment simulation with user parameters."""
    print("\n" + "=" * 50)
    print("RUNNING SIMULATION")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = BitcoinInvestmentAnalyzer('bitcoin_data.csv')
    
    if analyzer.data is None:
        print("Error: Could not load Bitcoin data")
        return
    
    display_data_info(analyzer)
    
    # Handle different date scenarios
    if params['choice'] == '3':
        # Calculate start date from most recent data
        latest_date = analyzer.data['Date'].max()
        start_date = latest_date - timedelta(days=params['days'])
        params['start_date'] = start_date
        print(f"\nCalculated start date: {start_date.strftime('%Y-%m-%d')}")
    
    # Display simulation parameters
    print(f"\nSimulation Parameters:")
    print(f"- Daily investment: ${params['daily_amount']:,.2f}")
    if params['start_date']:
        print(f"- Start date: {params['start_date'].strftime('%Y-%m-%d')}")
    if params['end_date']:
        print(f"- End date: {params['end_date'].strftime('%Y-%m-%d')}")
    if params['days']:
        print(f"- Investment period: {params['days']} days")
    
    # Run simulation
    try:
        results = analyzer.simulate_daily_investment(
            daily_amount=params['daily_amount'],
            start_date=params['start_date'],
            end_date=params['end_date'],
            days=params['days']
        )
        
        print(f"\n✓ Simulation completed successfully!")
        print(f"✓ Analyzed {len(results)} trading days")
        
        return analyzer
        
    except Exception as e:
        print(f"✗ Simulation failed: {e}")
        return None


def display_results(analyzer):
    """Display simulation results."""
    if analyzer is None:
        return
    
    # Print detailed summary
    analyzer.print_summary()
    
    # Get summary for additional analysis
    summary = analyzer.get_investment_summary()
    
    # Additional insights
    print(f"\nAdditional Insights:")
    print(f"- Average daily return: {(summary['return_percentage'] / summary['investment_days']):.4f}%")
    print(f"- Annualized return: {(summary['return_percentage'] * 365 / summary['investment_days']):.2f}%")
    
    if summary['return_percentage'] > 0:
        print(f"- Your investment would have grown by ${summary['total_return']:,.2f}")
    else:
        print(f"- Your investment would have lost ${abs(summary['total_return']):,.2f}")
    
    # Ask about visualization
    show_chart = input("\nWould you like to see the investment chart? (y/n): ").lower().strip()
    if show_chart == 'y':
        try:
            print("Generating chart...")
            analyzer.plot_investment_growth(figsize=(14, 10))
        except Exception as e:
            print(f"Error generating chart: {e}")
    
    # Ask about saving results
    save_chart = input("Would you like to save the chart to a file? (y/n): ").lower().strip()
    if save_chart == 'y':
        filename = input("Enter filename (e.g., my_analysis.png): ").strip()
        if not filename:
            filename = f"bitcoin_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        try:
            analyzer.plot_investment_growth(figsize=(14, 10), save_path=filename)
            print(f"Chart saved as: {filename}")
        except Exception as e:
            print(f"Error saving chart: {e}")


def main():
    """Main interactive function."""
    try:
        # Get user input
        params = get_user_input()
        
        # Run simulation
        analyzer = run_simulation(params)
        
        # Display results
        display_results(analyzer)
        
        # Ask if user wants to run another simulation
        print("\n" + "=" * 50)
        another = input("Would you like to run another simulation? (y/n): ").lower().strip()
        if another == 'y':
            print("\n")
            main()  # Recursive call for another simulation
        else:
            print("Thank you for using Bitcoin Investment Analyzer!")
    
    except KeyboardInterrupt:
        print("\n\nSimulation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check your inputs and try again.")


if __name__ == "__main__":
    main()