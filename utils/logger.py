import logging
import sys
import os

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    os.makedirs('logs', exist_ok=True)
    
    file_handler = logging.FileHandler('logs/integration.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger