import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from services.report_client import ReportClient
from utils.csv_generator import generate_csv
from utils.logger import setup_logger

logger = setup_logger("report_workflow")

def main():
    try:
        logger.info("Starting generating a report")
        
        csv_data = generate_csv()
        
        report_client = ReportClient()
        response = report_client.upload_csv(csv_data)
        
        result = {"success": True, "response": response, "message": "Success"}
        logger.info("Success")
        return result
        
    except Exception as e:
        error_msg = f"Error: {e}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

if __name__ == "__main__":
    result = main()
    print(str(result))