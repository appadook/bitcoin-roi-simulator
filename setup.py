#!/usr/bin/env python3
"""
Setup script for Bitcoin Investment Analyzer
"""

import subprocess
import sys
import os
from pathlib import Path


def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False


def download_sample_data():
    """Download sample Bitcoin data."""
    print("\nDownloading sample Bitcoin data...")
    try:
        from data_downloader import BitcoinDataDownloader
        downloader = BitcoinDataDownloader()
        
        # Try Yahoo Finance first (most reliable)
        success = downloader.download_yahoo_finance(period='2y', save_path='bitcoin_data.csv')
        
        if not success:
            print("Yahoo Finance failed, creating sample data...")
            success = downloader.create_sample_data(days=730, save_path='bitcoin_data.csv')
        
        if success:
            print("✓ Bitcoin data ready")
            return True
        else:
            print("✗ Failed to get Bitcoin data")
            return False
            
    except Exception as e:
        print(f"✗ Error downloading data: {e}")
        return False


def run_demo():
    """Run a quick demo of the analyzer."""
    print("\nRunning quick demo...")
    try:
        from bitcoin_investment_analyzer import BitcoinInvestmentAnalyzer
        
        analyzer = BitcoinInvestmentAnalyzer('bitcoin_data.csv')
        if analyzer.data is None:
            print("✗ No data available for demo")
            return False
        
        # Quick 30-day demo
        analyzer.simulate_daily_investment(daily_amount=10, days=30)
        summary = analyzer.get_investment_summary()
        
        print("\n" + "="*40)
        print("QUICK DEMO RESULTS")
        print("="*40)
        print(f"Investment: $10/day for 30 days")
        print(f"Total invested: ${summary['total_invested']:.2f}")
        print(f"Portfolio value: ${summary['final_portfolio_value']:.2f}")
        print(f"Return: {summary['return_percentage']:.2f}%")
        print("="*40)
        
        return True
        
    except Exception as e:
        print(f"✗ Demo failed: {e}")
        return False


def main():
    """Main setup function."""
    print("Bitcoin Investment Analyzer - Setup")
    print("="*40)
    
    # Check if we're in the right directory
    if not os.path.exists('bitcoin_investment_analyzer.py'):
        print("✗ Please run this script from the project directory")
        return
    
    print("This script will:")
    print("1. Install required Python packages")
    print("2. Download sample Bitcoin data")
    print("3. Run a quick demo")
    print()
    
    proceed = input("Continue? (y/n): ").lower().strip()
    if proceed != 'y':
        print("Setup cancelled")
        return
    
    # Step 1: Install requirements
    if not install_requirements():
        print("Setup failed at package installation")
        return
    
    # Step 2: Download data
    if not download_sample_data():
        print("Setup completed with warnings (no data available)")
        return
    
    # Step 3: Run demo
    if run_demo():
        print("\n✓ Setup completed successfully!")
        print("\nNext steps:")
        print("- Run 'python example_usage.py' for more examples")
        print("- Run 'python test_analyzer.py' for comprehensive testing")
        print("- Check README.md for detailed usage instructions")
    else:
        print("\n⚠ Setup completed but demo failed")
        print("You can still use the analyzer manually")


if __name__ == "__main__":
    main()