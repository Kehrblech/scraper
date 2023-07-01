import logging

logging.basicConfig(filename='logfile.txt', level=logging.INFO)

def log_to_file(url):
    logging.info(url)
