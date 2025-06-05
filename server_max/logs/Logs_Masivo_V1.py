import logging

def setup():
    logging.basicConfig(filename='server_max/logs/server_max.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
def log_info(message):
    setup()
    logging.info(f"[SERVIDOR INFO]: {message}")

def log_error(message):
    setup()
    logging.error(f"[SERVIDOR ERROR]: {message}")

def log_warning(message):
    setup()
    logging.warning(f"[SERVIDOR WARNING]: {message}")

def log_debug(message):
    setup()
    logging.debug(f"[SERVIDOR DEBUG]: {message}")

def log_critical(message):
    setup()
    logging.critical(f"[SERVIDOR CRITICAL]: {message}")
