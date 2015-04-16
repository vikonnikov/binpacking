import logging

log = logging.getLogger('base')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

def set_handler(handler_class):
    handler = handler_class()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    log.addHandler(handler)

def set_null_handler():
    set_handler(logging.NullHandler)

def set_console_handler():
    set_handler(logging.StreamHandler)

set_null_handler()