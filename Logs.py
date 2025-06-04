import logging

def setup():
    logging.basicConfig(filename='server.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
def log_info(message):
    logging.info(f"[SERVIDOR INFO]: {message}")

def log_error(message):
    logging.error(f"[SERVIDOR ERROR]: {message}")

def log_warning(message):
    logging.warning(f"[SERVIDOR WARNING]: {message}")

def log_debug(message):
    logging.debug(f"[SERVIDOR DEBUG]: {message}")

def log_critical(message):
    logging.critical(f"[SERVIDOR CRITICAL]: {message}")
