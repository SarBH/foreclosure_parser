# Foreclosure Parser

A Python tool to automatically scrape and track foreclosure property listings from Civil View, storing the data in Airtable.

## Features

- Automatically scrapes property listings from Civil View
- Extracts detailed property information
- Tracks status history
- Stores data in Airtable
- Implements caching to reduce server load
- Handles both new properties and updates
- Automated daily updates via GitHub Actions

## Prerequisites

Before you begin, ensure you have the following:

1. **Python 3.8 or higher**
   - Download from [Python's official website](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. **Google Chrome**
   - Download from [Chrome's official website](https://www.google.com/chrome/)

3. **Airtable Account**
   - Sign up at [Airtable](https://airtable.com/signup)
   - Create a new base with the following fields:
     * Sheriff Number (Single line text)
     * Case Number (Single line text)
     * Address (Single line text)
     * Sales Date (Single line text)
     * Plaintiff (Single line text)
     * Defendant (Single line text)
     * Description (Long text)
     * Judgment Amount (Number)
     * Good Faith Upset (Number)
     * Attorney (Single line text)
     * Attorney Phone (Single line text)
     * Status History (Long text)

## Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/foreclosure_parser.git
   cd foreclosure_parser
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Airtable**
   - Get your Airtable API key from your [account page](https://airtable.com/account)
   - Copy your Base ID and Table ID from the Airtable API documentation
   - Create a `.env` file in the project root with:
     ```
     AIRTABLE_API_KEY=your_api_key_here
     ```

## GitHub Actions Setup

The repository includes a GitHub Actions workflow that runs the scraper automatically every 24 hours. To set this up:

1. **Fork the repository** to your GitHub account

2. **Add GitHub Secret**
   - Go to your repository's Settings
   - Click on "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Name: `AIRTABLE_API_KEY`
   - Value: Your Airtable API key
   - Click "Add secret"

3. **Enable GitHub Actions**
   - Go to the "Actions" tab in your repository
   - Click "I understand my workflows, go ahead and enable them"

The scraper will now run automatically every day at midnight UTC (7:00 PM EST). You can also:
- Manually trigger the workflow from the Actions tab
- View run history and logs
- Download log files from each run

## Local Usage

1. **Activate the virtual environment** (if not already activated)
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Run the script**
   ```bash
   # On Windows
   python run.py

   # On macOS/Linux
   ./run.sh
   ```

The script will:
1. Scrape property listings from Civil View
2. Parse the data
3. Update Airtable with new/changed information
4. Create a log file with details of the operation

## Troubleshooting

### Common Issues

1. **Chrome Driver Error**
   - The script automatically downloads the correct Chrome driver
   - If you get an error, try updating Chrome to the latest version

2. **Airtable API Error**
   - Verify your API key is correct
   - Check your base and table IDs
   - Ensure your Airtable base has all required fields

3. **Permission Error**
   - On Linux/macOS, make sure run.sh is executable:
     ```bash
     chmod +x run.sh
     ```

4. **Module Not Found Error**
   - Ensure you've activated the virtual environment
   - Try reinstalling dependencies:
     ```bash
     pip install -r requirements.txt
     ```

### GitHub Actions Issues

1. **Workflow Not Running**
   - Check if Actions is enabled in your repository
   - Verify the AIRTABLE_API_KEY secret is set correctly
   - Check the workflow file syntax in `.github/workflows/daily_scrape.yml`

2. **Workflow Failing**
   - Check the workflow run logs in the Actions tab
   - Download the log artifact for detailed error messages
   - Verify Chrome is installing correctly in the workflow

### Getting Help

If you encounter any issues:
1. Check the log file (`property_scraper.log`)
2. Ensure all prerequisites are installed
3. Verify your configuration settings
4. Create an issue on GitHub with:
   - Error message
   - Log file contents
   - Your system information

## License

This project is licensed under the MIT License - see the LICENSE file for details.