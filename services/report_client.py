import requests
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ReportClient:
    def __init__(self):
        self.base_url = f"{settings.BASE_URL}/students/{settings.STUDENT_ID}"
    
    def upload_csv(self, csv_data: bytes) -> dict:
        try:
            headers = {
                'Content-Type': 'text/csv; charset=utf-8'
            }
            
            response = requests.post(
                f"{self.base_url}/report/csv",
                data=csv_data, 
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            logger.info("CSV successfully sent to Report API")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending CSV to Report API: {e}")
            raise Exception(f"Report API error: {e}")