"""Windows-compatible runner script for the foreclosure parser."""
import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if the environment is properly set up."""
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)

    # Load environment variables
    load_dotenv()
    
    # Check for Airtable API key
    if not os.getenv("AIRTABLE_API_KEY"):
        print("Error: AIRTABLE_API_KEY environment variable is not set")
        print("Please create a .env file with your Airtable API key")
        sys.exit(1)

if __name__ == "__main__":
    # Verify environment
    check_environment()
    
    # Import and run main after environment checks
    try:
        from src.main import main
        main()
    except ImportError as e:
        print(f"Error: Failed to import required modules. Please run 'pip install -r requirements.txt' first")
        print(f"Details: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)