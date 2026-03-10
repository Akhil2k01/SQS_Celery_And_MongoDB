"""
    This modules provide utility class for
    mongo connection class
"""
# pylint: disable=import-error
# pylint: disable=W1201
import logging
from mongoengine import connect

from config import Config


class CmConnection(object):  # pylint: disable=too-few-public-methods
    """
        This connection class helps us
        to create a context manager for
        mongo connection.
    """

    # pylint: disable=no-init
    def __enter__(self):
        """
            This special method creates a
            mongo connection using the context
            manager 'with'
        """
        # pylint: disable=attribute-defined-outside-init
        self.connection = connect(
            db=Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS,
            alias=Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS,
            host="{}{}".format(Config.MONGO_URI,
                               Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS)
        )
        logging.info("Connection Established %s" % Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS)
        print("Connection Established %s" % Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            This special method closes a
            the established mongo connection
            when all the mongo operation completes
        """
        self.connection.close()
        logging.info("Connection Closed %s" % Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS)
        print("Connection Closed %s" % Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS)