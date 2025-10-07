import csv
import io
from database.crud import DatabaseManager
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_csv() -> bytes:
    db = DatabaseManager()
    parts = db.get_parts_for_report()
    
    logger.info(f"Found {len(parts)} parts for CSV generation")
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', lineterminator='\n')
    
    for part in parts:
        
        writer.writerow([
            part.spare_code or '',
            part.spare_name or '',
            part.spare_description or '',
            part.spare_type or '',
            part.spare_status or '',
            format_price(part.price),
            part.quantity or 0,
            part.updated_at or ''
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    logger.info(f"Generated CSV with {len(parts)} rows, content preview: {csv_content}")
    return csv_content.encode('utf-8')


def format_price(price):
    if price is None:
        return '0'
    
    try:
        price_float = float(price)
        if price_float.is_integer():
            return str(int(price_float))
        else:
            return str(price_float)
    except (ValueError, TypeError):
        return '0'
