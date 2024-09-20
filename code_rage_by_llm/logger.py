import logging

def setup_logger():
    logger = logging.getLogger('code_indexer')
    
    # 检查是否已经添加了处理器，如果有，就不再添加
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('code_indexer.log')
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# 创建一个全局的 logger 实例
logger = setup_logger()