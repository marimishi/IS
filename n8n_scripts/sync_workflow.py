import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from services.sync_service import SyncService
from utils.logger import setup_logger

logger = setup_logger("sync_workflow")

def main():
    try:
        sync_service = SyncService()
        count = sync_service.sync_data()
        
        result = {"success": True, "count": count, "message": f"Success {count}"}
        logger.info(f"Success {count}")
        return result
        
    except Exception as e:
        error_msg = f"Error: {e}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

if __name__ == "__main__":
    result = main()
    print(str(result))