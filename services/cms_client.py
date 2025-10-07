import requests
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class CMSClient:
    def __init__(self):
        self.base_url = f"{settings.BASE_URL}/students/{settings.STUDENT_ID}"
    
    def get_spare_parts(self, page: int = 0, size: int = 10) -> list:
        try:
            logger.info(f"Query from CMS API - page {page}, size {size}")
            response = requests.get(
                f"{self.base_url}/cms/spares?page={page}&size={size}", 
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"Got {len(data)} parts from page {page}")
            return data
        except requests.RequestException as e:
            logger.error(f"Error CMS API: {e}")
            raise Exception(f"CMS API error: {e}")
    
    def get_all_spare_parts(self, page_size: int = 10) -> list:
        all_parts = []
        page = 0
        
        while True:
            try:
                parts = self.get_spare_parts(page=page, size=page_size)
                
                if not parts:
                    logger.info(f"No more parts found on page {page}")
                    break
                
                all_parts.extend(parts)
                logger.info(f"Page {page}: got {len(parts)} parts, total: {len(all_parts)}")
                
                if len(parts) < page_size:
                    logger.info(f"Last page reached - got {len(parts)} parts, expected {page_size}")
                    break
                
                page += 1
                
            except Exception as e:
                logger.error(f"Error getting page {page}: {e}")
                break
        
        logger.info(f"Total parts collected: {len(all_parts)}")
        return all_parts