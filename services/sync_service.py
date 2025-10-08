from database.crud import DatabaseManager
from services.cms_client import CMSClient
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SyncService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.cms_client = CMSClient()
    
    def sync_data(self) -> int:
        try:
            current_parts = self.cms_client.get_all_spare_parts(page_size=10)
            
            count = self.db_manager.update_spare_parts(
                current_parts, 
                settings.SYNC_PERIOD
            )
            
            logger.info(f"Success. Updated {count} parts from {len(current_parts)} total parts")
            return count
            
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            raise