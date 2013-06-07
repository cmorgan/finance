
import logging


def init_logging():
    'Initialise root logger using config settings.'
    logging.basicConfig(
        level='INFO',
        format='%(asctime)-15s %(levelname)-8s %(module)s %(message)s',
    )
