import logging

log_level = logging.DEBUG
# log_level = logging.WARNING
# log_level = logging.CRITICAL
# log_level = logging.ERROR

logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=log_level)
